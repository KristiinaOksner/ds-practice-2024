# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fraud_detection.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\x0f\x66raud_detection\"6\n\x15\x46raudDetectionRequest\x12\x0f\n\x07\x63ountry\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\"?\n\x16\x46raudDetectionResponse\x12\x15\n\ris_fraudulent\x18\x01 \x01(\x08\x12\x0e\n\x06reason\x18\x02 \x01(\t2x\n\x15\x46raudDetectionService\x12_\n\nCheckFraud\x12&.fraud_detection.FraudDetectionRequest\x1a\'.fraud_detection.FraudDetectionResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FRAUDDETECTIONREQUEST']._serialized_start=42
  _globals['_FRAUDDETECTIONREQUEST']._serialized_end=96
  _globals['_FRAUDDETECTIONRESPONSE']._serialized_start=98
  _globals['_FRAUDDETECTIONRESPONSE']._serialized_end=161
  _globals['_FRAUDDETECTIONSERVICE']._serialized_start=163
  _globals['_FRAUDDETECTIONSERVICE']._serialized_end=283
# @@protoc_insertion_point(module_scope)
