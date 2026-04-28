import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Configure API base URL
const api = axios.create({ baseURL: 'http://localhost:8000' }) // FastAPI default backend url

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }
