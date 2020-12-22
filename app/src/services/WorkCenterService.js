import axios from 'axios'

class WorkCenterService {
    defaultOptions = { 
        headers: { 
            'Content-Type': 'application/json' 
        } 
    };
    defaultUrl = "http://localhost";

    async getWorkCenters() {
      const response = await axios.get(`${defaultUrl}/work-centers`, this.defaultOptions)
      return response.data
    }

    async getExpeditions() {
      const response = await axios.get(`${defaultUrl}/expeditions`, this.defaultOptions)
      return response.data
    }

    async getAttendence() {
      const response = await axios.get(`${defaultUrl}/attendence`, this.defaultOptions)
      return response.data
    }

    async sendExpeditionWithPredition() {
        const response = await axios.post(`${defaultUrl}/expeditions`, 
            { 
                work_center_id: work_center.id, 
                auto_predict_qty_needed: true
            },
            this.defaultOptions)

        return response.data
    }
}

export default WorkCenterService