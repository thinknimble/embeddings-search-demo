import csv
import glob
import html
import logging
import os
import re
import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from pgvector.django import L2Distance, VectorField
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from vector_demonstration.common.models import AbstractBaseModel
from vector_demonstration.utils.sites import get_site_url

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """Custom User model manager, eliminating the 'username' field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.

        All emails are lowercased automatically.
        """
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        logger.info(f"New user: {email}")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser with the given email and password."""
        logger.warning(f"Creating superuser: {email}")
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["has_reset_password"] = True
        return self._create_user(email, password, **extra_fields)

    class Meta:
        ordering = ("id",)


class User(AbstractUser, AbstractBaseModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    has_reset_password = models.BooleanField(default=False)
    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    def reset_password_context(self):
        return {
            "user": self,
            "site_url": get_site_url(),
            "support_email": settings.STAFF_EMAIL,
            "token": default_token_generator.make_token(self),
        }

    class Meta:
        ordering = ["email"]


class JobDescription(AbstractBaseModel):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    language = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def import_job_descriptions(cls):
        def get_jobs_csv():
            """Find all the CSV files in the jobs directory and return them as a generator"""
            data_directory = os.path.join(settings.BASE_DIR, "..", "..", "data", "jobs")
            csv_paths = glob.glob(f"{data_directory}/*.csv")
            for csv_path in csv_paths:
                with open(csv_path, "r") as f:
                    yield f

        for csvfile in get_jobs_csv():
            print(f"Loading {csvfile.name}...")
            start_time = time.time()

            csvreader = csv.DictReader(csvfile, delimiter=",")

            job_descriptions = []
            for row in csvreader:
                # try:
                #     language = detect(row["description"])
                # except LangDetectException:
                #     language = ""
                job_descriptions.append(
                    cls(
                        title=row["title"],
                        company=row["company"],
                        location=row["location"],
                        description=row["description"],
                        skills=row["skills"],
                        # language=language,
                    )
                )

            cls.objects.bulk_create(job_descriptions)

            print(f"    Loaded in {time.time() - start_time} seconds.")

    @classmethod
    def detect_languages(cls):
        def get_job_descriptions():
            page_size = 1000
            num_pages = cls.objects.count() // page_size + 1
            for page in range(num_pages):
                qs = cls.objects.filter(language="")[page * page_size : (page + 1) * page_size]
                for job_description in qs:
                    yield job_description

        count = 0
        total_jds = cls.objects.filter(language="").count()
        for job_description in get_job_descriptions():
            count += 1
            print(f"Detecting language for JD #{count} of {total_jds}...")
            try:
                language = detect(job_description.description)
            except LangDetectException:
                language = ""
            job_description.language = language
            job_description.save()

    def generate_embeddings(self):
        def strip_html_tags(text):
            tag_re = re.compile(r"(<!--.*?-->|<[^>]*>)")
            no_tags = tag_re.sub("", text)
            return html.escape(no_tags)

        def get_chunks(jd_content, chunk_size=750):
            """Naive chunking of job description.

            `chunk_size` is the number of characters per chunk.
            """
            chunk_size = chunk_size
            content = strip_html_tags(jd_content).replace("\n", " ")
            while content:
                chunk, content = content[:chunk_size], content[chunk_size:]
                yield chunk

        # 1. Set up the embedding model
        model = SentenceTransformer("all-MiniLM-L6-v2")
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        # 2. Chunk the job description into sentences
        chunk_embeddings = ((c, tokenizer.tokenize(c), model.encode(c)) for c in get_chunks(self.description))

        # 3. Save the embeddings information for each chunk
        jd_chunks = []
        for chunk_content, chunk_tokens, chunk_embedding in chunk_embeddings:
            jd_chunks.append(
                JobDescriptionChunk(
                    job_description=self,
                    chunk=chunk_content,
                    token_count=len(chunk_tokens),
                    embedding=chunk_embedding,
                )
            )

        JobDescriptionChunk.objects.bulk_create(jd_chunks)

    @classmethod
    def search(cls, query=None):
        query = (
            query
            or "The student would prefer a job in the arts. They have a background in choir and theater. Major: Music. Minor: Theater. Graduating Year: 2022"
        )
        # > expected result: list of Job Descriptions in descending order of relevance
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode(query)

        jd_chunks = JobDescriptionChunk.objects.annotate(distance=L2Distance("embedding", query_embedding)).order_by("distance")

        unique_jds = {}
        for chunk in jd_chunks:
            if chunk.job_description.id not in unique_jds:
                unique_jds[chunk.job_description.id] = {
                    "job_description": chunk.job_description,
                    "chunks": [chunk],
                }
            else:
                unique_jds[chunk.job_description.id]["chunks"].append(chunk)

        results = []
        for k, v in unique_jds.items():
            score = sum([c.distance for c in v["chunks"]]) / len(v["chunks"])
            job_description = v["job_description"]
            results.append(JobDescriptionSearchResult(score, job_description, v["chunks"]))

        return sorted(results, key=lambda r: r.score)


class JobDescriptionChunk(AbstractBaseModel):
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="chunks")
    chunk = models.TextField()
    token_count = models.IntegerField(null=True)
    embedding = VectorField(dimensions=384)

    def __str__(self):
        return f"{self.job_description.title} - {self.chunk[:50]}"


class JobDescriptionSearchResult:
    def __init__(self, score, job_description, chunks):
        self.score = score
        self.job_description = job_description
        self.chunks = chunks

    def __str__(self):
        return f"{self.score}: {self.job_description.title}"
