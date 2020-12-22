function WorkCenterCard(props){
  const colors = {
    'Vermelha': 'bg-danger',
    'Amarela': 'bg-warning',
    'Verde': 'bg-success',
  }

  return (
    <div className={`card text-white ${colors[props.work_center.coverage_classification]} mb-3`} Style={"max-width: 18rem;"}>
      <div className={`card-header ${colors[props.work_center.coverage_classification]}`}>
        <h4>{props.work_center.region}</h4>
      </div>
      <div className="card-body">
        <p className="card-text">
          {props.work_center.days_of_coverage} Dias de cobertura <br></br>
          <b>Média de Atendimentos:</b> {props.work_center.avg_of_attendence} <br></br>
          <b>Qt. Disponível: </b> {props.work_center.qty_of_terminals_available} <br></br>

          <button class="btn btn-outline-light btn-block btn-round mt-4">
            Enviar Expedição
          </button>
        </p>
      </div>
    </div>
  )
}

export default WorkCenterCard