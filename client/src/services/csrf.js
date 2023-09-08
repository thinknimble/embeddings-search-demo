import Cookies from 'js-cookie'

export default {
  getToken() {
    return Cookies.get('csrftoken')
  },
  getHeaders() {
    return {
      'Content-Type': 'application/json',
      'X-CSRFToken': this.getToken(),
    }
  },
}
