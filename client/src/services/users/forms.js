import Form, {
  FormField,
  MinLengthValidator,
  MustMatchValidator,
  RequiredValidator,
  EmailValidator,
} from '@thinknimble/tn-forms'

export class LoginForm extends Form {
  static email = new FormField({ validators: [new RequiredValidator(), new EmailValidator()] })
  static password = new FormField({ validators: [new RequiredValidator()] })
}

export class SignupForm extends Form {
  static firstName = new FormField({ validators: [new RequiredValidator()] })
  static lastName = new FormField({ validators: [new RequiredValidator()] })
  static email = new FormField({ validators: [new RequiredValidator(), new EmailValidator()] })
  static password = new FormField({
    validators: [new MinLengthValidator({ minLength: 8, message: 'Minimum Length of 8 required' })],
  })
  static confirmPassword = new FormField({})
  // add cross field validators to the dynamicFormValidators object
  static dynamicFormValidators = {
    confirmPassword: [new MustMatchValidator({ matcher: 'password' })],
  }
}

export class RequestPasswordResetForm extends Form {
  static email = new FormField({ validators: [new RequiredValidator(), new EmailValidator()] })
}

export class PasswordResetForm extends Form {
  static password = new FormField({
    validators: [
      new RequiredValidator(),
      new MinLengthValidator({ minLength: 8, message: 'Minimum Length of 8 required' }),
    ],
  })
  static confirmPassword = new FormField({})
  static dynamicFormValidators = {
    confirmPassword: [new MustMatchValidator({ matcher: 'password' })],
  }
}
