function AttendanceItemList(props) {
    return (
      <tr>
        <td>{props.attendance.id}</td>
        <td>{props.attendance.work_center.region}</td>
        <td>{props.attendance.qty_of_terminals}</td>
        <td>{props.attendance.was_canceled ? 'Sim' : 'Não'}</td>
      </tr>
    );
}

export default AttendanceItemList