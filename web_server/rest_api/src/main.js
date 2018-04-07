// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

new Vue({
  el: '#app2',
  data: {
    rec_bands: '',
    user_id: ''
  },
  delimiters: ['[[', ']]'],
  methods: {
    get_rec_bands: function () {
      var user = {user_id: this.user_id}
      axios.post('http://localhost:8000/get_rec_bands/', user).then(response => {
        this.rec_bands = response.data
      })
    }

  }
})
