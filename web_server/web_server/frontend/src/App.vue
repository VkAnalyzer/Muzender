<template>
  <div>
    <input v-model="user_id" placeholder="Enter vk.com profile">
      <button v-on:click="get_rec_bands()">
        <span>Recommend me some cool music</span>
      </button>
    <p v-show="rec_bands">We recommend you to listen the following bands:</p>
      <ul>
        <li v-for="band in rec_bands">
          {{ band }}
        </li>
      </ul>
  </div>
</template>

<script>
import {MuzenderAPI} from './API/MuzenderAPI'

const muzender_api = new MuzenderAPI()

export default {
  name: 'app',
  data() {
    return {
      rec_bands: '',
      user_id: '',
      loading: false
    };
  },
  methods: {
    get_rec_bands() {
      let user = {user_id: this.user_id}
      this.loading = true
      muzender_api.get_rec_bands(user).then((response_data) => {
        this.rec_bands = response_data
        this.loading = false
      })
    }
  }
}
</script>
