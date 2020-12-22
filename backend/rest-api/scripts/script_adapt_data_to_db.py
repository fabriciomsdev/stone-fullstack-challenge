import csv
from data.data_source import DBDataSource
from data.models import (
    WorkCentersModel, 
    ExpeditionsModel, 
    AttendanceModel
)
from datetime import datetime
import multiprocessing as mp
from use_cases.work_centers import WorkCentersUseCases


ds = DBDataSource()

db_conn = ds.connect_to_source('sqlite:///db.sqlite3')
db_session = db_conn.create_a_session()
wc_table = db_session.query(WorkCentersModel)
expedition_table = db_session.query(ExpeditionsModel)
attendance_table = db_session.query(AttendanceModel)
wc_region_model_dict = {}
wc_id_n_attendance_dict = {}
wc_expeditions_increment = {}
work_center_use_case = WorkCentersUseCases(ds)

def open_csv_file(filename: str):
    input_file = csv.DictReader(open(filename))
    return list(input_file)


def save_a_wc_by_dict(wc: dict):
    wc_model = WorkCentersModel(region=wc.get('region'))
    db_session.add(wc_model)

    return wc_model


print("Clear DB -> ")

ds.clear(ignore_foreign_keys=False)

print("Work Centers Registred -> ", len(wc_table.all()))

attendance_in_csv = open_csv_file('./../temp/challenge-data/attendance-data.csv')
work_centers_in_csv = open_csv_file('./../temp/challenge-data/expeditions_after_load.csv')
wcs_ids_allowed = [1, 3, 4, 12, 14, 15]

for wc in work_centers_in_csv:
    if wc.get('region') is not None:
        wc_model = save_a_wc_by_dict(wc)
        wc_region_model_dict[wc_model.region] = wc_model
        wc_expeditions_increment[wc_model.region] = wc.get(
            'first_expedition')

        print("Was added -> ", wc_model.region,
                wc_model.id, wc.get('first_expedition'))

print("Commit WCs -> ")

db_session.commit()

print("Registering attendance -> ", len(attendance_in_csv))

counter = 0
for attdc in attendance_in_csv:
    wc_for_attdc = wc_region_model_dict.get(attdc.get('region'))

    if (wc_for_attdc.id in wcs_ids_allowed):
        if wc_for_attdc is None:
            wc_for_attdc = save_a_wc_by_dict(attdc)
            db_session.commit()
            print("Not found and force register:",
                    attdc.get('region'))

        attdc_model = AttendanceModel(
            work_center=wc_for_attdc,
            qty_of_terminals=attdc.get('qty_of_terminals'),
            attendance_date=datetime.strptime(attdc.get('date'), '%Y-%m-%d'),
            was_canceled=False
        )

        db_session.add(attdc_model)
        counter += 1

        if wc_id_n_attendance_dict.get(wc_for_attdc.id) is None:
            wc_id_n_attendance_dict[wc_for_attdc.id] = 1
        else:
            wc_id_n_attendance_dict[wc_for_attdc.id] += 1

        print("Register attandance -> WC ", wc_for_attdc.id, counter, " ",
                attdc.get('region'), attdc.get('date'))

        if counter % 100 == 0:
            db_session.commit()
            print("Send to DB -> ", counter, " ", attdc_model.__dict__)

    print("Registering expeditions -> ")

wcs = wc_region_model_dict.values()

for wc_in_db in wcs:
    if wc_in_db.id in wcs_ids_allowed:
        first_expd_terms = wc_expeditions_increment[wc_in_db.region]

        if first_expd_terms is None:
            first_expd_terms = 0

        terminals_qty = int(wc_id_n_attendance_dict.get(
            wc_in_db.id)) + int(first_expd_terms)
        last_expedition = ExpeditionsModel(
            work_center=wc_in_db,
            qty_of_terminals=terminals_qty,
            was_canceled=False
        )

        db_session.add(last_expedition)
        print("Expedition register -> ", terminals_qty, wc_in_db.region)

print("Expedition register COMMIT ")

db_session.commit()

print("Expedition register FINISHED ")


for wc_in_db in wc_table.all():
    wc_in_db = work_center_use_case.update_calculated_values(wc_in_db)
    print('updated wc ->', wc_in_db.qty_of_terminals_available,
          wc_in_db.qty_of_terminals_used)


#ds.clear(ignore_foreign_keys=True)
