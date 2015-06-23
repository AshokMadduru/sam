##from google.appengine.api.files import records
##from google.appengine.datastore import entity_pb
##from google.appengine.api import datastore
 
raw = open('C:\Users\ASHOK\Downloads\Metadata_Backup\Metadata_Backup/datastore_backup_metadata_backup_2015_05_01_Meta-1574939762280AE6C3143-output-0-attempt-1', 'r')
reader = records.RecordsReader(raw)
for record in reader:
        entity_proto = entity_pb.EntityProto(contents=record)
        entity = datastore.Entity.FromPb(entity_proto)
