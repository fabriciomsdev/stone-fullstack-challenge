import React, { Component } from 'react'
import ExpeditionItemList from './ExpeditionItemList'
import WorkCenterCard from './WorkCentersCard'
import AttendanceItemList from './AttendanceItemList'

class Dashboard extends Component {

  
  store = {
      work_centers: [
          {
              "attendance": [],
              "avg_of_attendence": 0,
              "coverage_classification": "Verde",
              "days_of_coverage": 0,
              "days_qty_ideal_for_coverage": 14,
              "expeditions": [
                  {
                      "auto_predict_qty_needed": null,
                      "id": 1,
                      "qty_of_terminals": 1000,
                      "was_canceled": false
                  },
                  {
                      "auto_predict_qty_needed": null,
                      "id": 2,
                      "qty_of_terminals": 1000,
                      "was_canceled": false
                  },
                  {
                      "auto_predict_qty_needed": null,
                      "id": 3,
                      "qty_of_terminals": 1000,
                      "was_canceled": false
                  }
              ],
              "id": 1,
              "qty_of_terminals_available": 3000,
              "qty_of_terminals_received": 3000,
              "qty_of_terminals_used": 0,
              "region": "NY 2 - New York"
          },
          {
              "attendance": [],
              "avg_of_attendence": 0,
              "coverage_classification": "Vermelha",
              "days_of_coverage": 0,
              "days_qty_ideal_for_coverage": 14,
              "expeditions": [],
              "id": 2,
              "qty_of_terminals_available": 0,
              "qty_of_terminals_received": 0,
              "qty_of_terminals_used": 0,
              "region": "NY 2 - New York"
          },
          {
              "attendance": [],
              "avg_of_attendence": 0,
              "coverage_classification": "Vermelha",
              "days_of_coverage": 0,
              "days_qty_ideal_for_coverage": 14,
              "expeditions": [],
              "id": 3,
              "qty_of_terminals_available": 0,
              "qty_of_terminals_received": 0,
              "qty_of_terminals_used": 0,
              "region": "NY 2 - New York"
          },
          {
              "attendance": [],
              "avg_of_attendence": 0,
              "coverage_classification": "Vermelha",
              "days_of_coverage": 0,
              "days_qty_ideal_for_coverage": 14,
              "expeditions": [],
              "id": 4,
              "qty_of_terminals_available": 0,
              "qty_of_terminals_received": 0,
              "qty_of_terminals_used": 0,
              "region": "NY 2 - New York"
          }
      ],
      expeditions: [
          {
              "auto_predict_qty_needed": null,
              "id": 1,
              "qty_of_terminals": 1000,
              "was_canceled": false,
              "work_center": {
                  "avg_of_attendence": 0,
                  "coverage_classification": "Verde",
                  "days_of_coverage": 0,
                  "days_qty_ideal_for_coverage": 14,
                  "id": 1,
                  "qty_of_terminals_available": 3000,
                  "qty_of_terminals_received": 3000,
                  "qty_of_terminals_used": 0,
                  "region": "NY 2 - New York"
              }
          },
          {
              "auto_predict_qty_needed": null,
              "id": 2,
              "qty_of_terminals": 1000,
              "was_canceled": false,
              "work_center": {
                  "avg_of_attendence": 0,
                  "coverage_classification": "Verde",
                  "days_of_coverage": 0,
                  "days_qty_ideal_for_coverage": 14,
                  "id": 1,
                  "qty_of_terminals_available": 3000,
                  "qty_of_terminals_received": 3000,
                  "qty_of_terminals_used": 0,
                  "region": "NY 2 - New York"
              }
          },
          {
              "auto_predict_qty_needed": null,
              "id": 3,
              "qty_of_terminals": 1000,
              "was_canceled": false,
              "work_center": {
                  "avg_of_attendence": 0,
                  "coverage_classification": "Verde",
                  "days_of_coverage": 0,
                  "days_qty_ideal_for_coverage": 14,
                  "id": 1,
                  "qty_of_terminals_available": 3000,
                  "qty_of_terminals_received": 3000,
                  "qty_of_terminals_used": 0,
                  "region": "NY 2 - New York"
              }
          }
      ],
      attendance: []
    }

  render() {
    return (
      <div className="content">
        <div className="container-fluid">
          <h3 className="card-title">Polos:</h3>
            <div className="row">
                {this.store.work_centers.map((work_center, index) => (
                  <div className="col-md-3">
                    <WorkCenterCard work_center={work_center} ></WorkCenterCard>
                  </div>
                ))}
            </div>
          <div className="row">

            <div className="col-md-6">
              <div className="card ">
                <div className="card-header ">
                  <h4 className="card-title">Expedições enviadas</h4>
                </div>
                <div className="card-body ">
                  <div class="table-responsive table-full-width">
                    <table class="table table-hover table-striped">
                      <thead>
                        <th>ID</th>
                        <th>Polo</th>
                        <th>Qt. de Terminais</th>
                        <th>Cancelada</th>
                      </thead>
                      <tbody>
                          {this.store.expeditions.map((expedition, index) => (
                            <ExpeditionItemList expedition={expedition} ></ExpeditionItemList>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            
            </div>
            <div className="col-md-6">
              <div className="card ">
                <div className="card-header ">
                  <h4 className="card-title">Atendimentos Realizados</h4>
                </div>
                <div className="card-body ">
                  <div class="table-responsive table-full-width">
                    <table class="table table-hover table-striped">
                      <thead>
                        <th>ID</th>
                        <th>Polo</th>
                        <th>Qt. de Terminais</th>
                        <th>Cancelado</th>
                      </thead>
                      <tbody>
                          {this.store.expeditions.map((attendance, index) => (
                            <AttendanceItemList attendance={attendance} ></AttendanceItemList>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Dashboard