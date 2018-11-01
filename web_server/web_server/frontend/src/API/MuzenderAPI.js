import axios from 'axios'

const API_URL = 'http://localhost:8000'

export class MuzenderAPI{
  constructor() {}
  get_rec_bands(user) {
    const url = `${API_URL}/get_rec_bands/`;
    return axios.post(url, user).then(response => response.data);
  }
}
