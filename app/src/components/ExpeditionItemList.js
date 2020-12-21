function ExpeditionItemList(props) {
    return (
      <tr>
        <td>{props.expedition.id}</td>
        <td>{props.expedition.work_center.region}</td>
        <td>{props.expedition.qty_of_terminals}</td>
        <td>{props.expedition.was_canceled ? 'Sim' : 'Não'}</td>
      </tr>
    );
}

export default ExpeditionItemList