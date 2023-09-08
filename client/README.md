# Vue3

## Favicon Setup

The Django app is already configured to serve favorite icons for all browsers and platforms (include, for example, apple-icons and android-icons at various sizes). By default, this icon is the TN logo.

**_Note your image must be a square otherwise a white bg will appear because the file is cropped if it is not a square go to [iloveimg.com](https://www.iloveimg.com/resize-image) and resize it._**
Visit [favicon-generator.org](https://www.favicon-generator.org/) and upload a high resolution, square version of the image you would like to use as the favicon for this app.

Download the ZIP file of icons that the site generates for you and paste them in the `client/public/static/favicons/` directory.

When we run collectstatic the public folder is copied as is and enables serving of the favicons

## Logo Setup

Swap out the logo files in these locations:
`client/src/assets/icons/glyph.svg` (Used by the webapp)
`server/vector_demonstration/core/static/images/logo.png` (Used by HTML emails)

## Initial Setup for non-Docker local

First, create `.env.local` at the top-level of the **client** directory, and copy the contents of `.env.local.example` into it.
Un-comment the value of `VUE_APP_DEV_SERVER_BACKEND` that is appropriate for your situation.

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Run your unit tests

```
npm run test:unit
```

### Run your end-to-end tests

```
npm run test:e2e
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

### This use vue3

Vue 3 was entirely re-written from scratch by the core team, the new version is written in ts and includes a number of new features. There are some breaking changes that have been addressed in the bootstrapper (in terms of initialization). Although Vue has added an entirely new api for most of its framework, the vue2 way of doing things can still be used. One major change was the [Composition Api](https://v3.vuejs.org/api/composition-api.html) (modeled of react hooks) that adds a functional approach to component composition (previously it was called the Options Api). There are additional features for example users can add multiple root elements instead of one wrapping div. Additionally Vue3 removes the 'magic' element and returns control to the dev, since this layer has been removed you will notice a major change when accessing [reactive](https://v3.vuejs.org/api/reactivity-api.html) variables (props, data, computed, watchers) they are instead returend in a wrapped obejct called a proxy, as a quick way of overcoming this new syntax there is a helper method called unwrap in the utils.js file that unwraps the object. You can also use a simple es6 spread operator however this will not work for nested reactive variables, the unwrap method handles this.
