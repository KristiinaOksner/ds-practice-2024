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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\x0f\x66raud_detection\"6\n\x0c\x43heckRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x15\n\rorder_amounts\x18\x02 \x03(\x01\";\n\x12\x46raudCheckResponse\x12\x15\n\ris_fraudulent\x18\x01 \x01(\x08\x12\x0e\n\x06reason\x18\x02 \x01(\t2d\n\x0e\x46raudDetection\x12R\n\nCheckFraud\x12\x1d.fraud_detection.CheckRequest\x1a#.fraud_detection.FraudCheckResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CHECKREQUEST']._serialized_start=42
  _globals['_CHECKREQUEST']._serialized_end=96
  _globals['_FRAUDCHECKRESPONSE']._serialized_start=98
  _globals['_FRAUDCHECKRESPONSE']._serialized_end=157
  _globals['_FRAUDDETECTION']._serialized_start=159
  _globals['_FRAUDDETECTION']._serialized_end=259
# @@protoc_insertion_point(module_scope)
