# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/core/v1/handler.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/core/v1/handler.proto',
  package='spaceone.api.core.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\"spaceone/api/core/v1/handler.proto\x12\x14spaceone.api.core.v1\x1a\x1cgoogle/protobuf/struct.proto\"\xd0\x02\n\x14\x41uthorizationRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\x12\x0c\n\x04verb\x18\x03 \x01(\t\x12?\n\x05scope\x18\x04 \x01(\x0e\x32\x30.spaceone.api.core.v1.AuthorizationRequest.Scope\x12\x11\n\tdomain_id\x18\x05 \x01(\t\x12\x12\n\nproject_id\x18\x06 \x01(\t\x12\x18\n\x10project_group_id\x18\x07 \x01(\t\x12\x0f\n\x07user_id\x18\x08 \x01(\t\x12\x1a\n\x12require_project_id\x18\t \x01(\x08\x12 \n\x18require_project_group_id\x18\n \x01(\x08\"6\n\x05Scope\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06SYSTEM\x10\x01\x12\n\n\x06\x44OMAIN\x10\x02\x12\x0b\n\x07PROJECT\x10\x03\"T\n\x15\x41uthorizationResponse\x12\x11\n\trole_type\x18\x01 \x01(\t\x12\x10\n\x08projects\x18\x02 \x03(\t\x12\x16\n\x0eproject_groups\x18\x03 \x03(\t\"*\n\x15\x41uthenticationRequest\x12\x11\n\tdomain_id\x18\x01 \x01(\t\"?\n\x16\x41uthenticationResponse\x12\x11\n\tdomain_id\x18\x01 \x01(\t\x12\x12\n\npublic_key\x18\x02 \x01(\t\"y\n\x0c\x45ventRequest\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x10\n\x08resource\x18\x02 \x01(\t\x12\x0c\n\x04verb\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12(\n\x07message\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Structb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])



_AUTHORIZATIONREQUEST_SCOPE = _descriptor.EnumDescriptor(
  name='Scope',
  full_name='spaceone.api.core.v1.AuthorizationRequest.Scope',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SYSTEM', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DOMAIN', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PROJECT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=373,
  serialized_end=427,
)
_sym_db.RegisterEnumDescriptor(_AUTHORIZATIONREQUEST_SCOPE)


_AUTHORIZATIONREQUEST = _descriptor.Descriptor(
  name='AuthorizationRequest',
  full_name='spaceone.api.core.v1.AuthorizationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='service', full_name='spaceone.api.core.v1.AuthorizationRequest.service', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource', full_name='spaceone.api.core.v1.AuthorizationRequest.resource', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='verb', full_name='spaceone.api.core.v1.AuthorizationRequest.verb', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scope', full_name='spaceone.api.core.v1.AuthorizationRequest.scope', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.core.v1.AuthorizationRequest.domain_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_id', full_name='spaceone.api.core.v1.AuthorizationRequest.project_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_group_id', full_name='spaceone.api.core.v1.AuthorizationRequest.project_group_id', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='spaceone.api.core.v1.AuthorizationRequest.user_id', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='require_project_id', full_name='spaceone.api.core.v1.AuthorizationRequest.require_project_id', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='require_project_group_id', full_name='spaceone.api.core.v1.AuthorizationRequest.require_project_group_id', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _AUTHORIZATIONREQUEST_SCOPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=91,
  serialized_end=427,
)


_AUTHORIZATIONRESPONSE = _descriptor.Descriptor(
  name='AuthorizationResponse',
  full_name='spaceone.api.core.v1.AuthorizationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='role_type', full_name='spaceone.api.core.v1.AuthorizationResponse.role_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='projects', full_name='spaceone.api.core.v1.AuthorizationResponse.projects', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='project_groups', full_name='spaceone.api.core.v1.AuthorizationResponse.project_groups', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=429,
  serialized_end=513,
)


_AUTHENTICATIONREQUEST = _descriptor.Descriptor(
  name='AuthenticationRequest',
  full_name='spaceone.api.core.v1.AuthenticationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.core.v1.AuthenticationRequest.domain_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=515,
  serialized_end=557,
)


_AUTHENTICATIONRESPONSE = _descriptor.Descriptor(
  name='AuthenticationResponse',
  full_name='spaceone.api.core.v1.AuthenticationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.core.v1.AuthenticationResponse.domain_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='public_key', full_name='spaceone.api.core.v1.AuthenticationResponse.public_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=559,
  serialized_end=622,
)


_EVENTREQUEST = _descriptor.Descriptor(
  name='EventRequest',
  full_name='spaceone.api.core.v1.EventRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='service', full_name='spaceone.api.core.v1.EventRequest.service', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource', full_name='spaceone.api.core.v1.EventRequest.resource', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='verb', full_name='spaceone.api.core.v1.EventRequest.verb', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='spaceone.api.core.v1.EventRequest.status', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='spaceone.api.core.v1.EventRequest.message', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=624,
  serialized_end=745,
)

_AUTHORIZATIONREQUEST.fields_by_name['scope'].enum_type = _AUTHORIZATIONREQUEST_SCOPE
_AUTHORIZATIONREQUEST_SCOPE.containing_type = _AUTHORIZATIONREQUEST
_EVENTREQUEST.fields_by_name['message'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name['AuthorizationRequest'] = _AUTHORIZATIONREQUEST
DESCRIPTOR.message_types_by_name['AuthorizationResponse'] = _AUTHORIZATIONRESPONSE
DESCRIPTOR.message_types_by_name['AuthenticationRequest'] = _AUTHENTICATIONREQUEST
DESCRIPTOR.message_types_by_name['AuthenticationResponse'] = _AUTHENTICATIONRESPONSE
DESCRIPTOR.message_types_by_name['EventRequest'] = _EVENTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AuthorizationRequest = _reflection.GeneratedProtocolMessageType('AuthorizationRequest', (_message.Message,), {
  'DESCRIPTOR' : _AUTHORIZATIONREQUEST,
  '__module__' : 'spaceone.api.core.v1.handler_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.core.v1.AuthorizationRequest)
  })
_sym_db.RegisterMessage(AuthorizationRequest)

AuthorizationResponse = _reflection.GeneratedProtocolMessageType('AuthorizationResponse', (_message.Message,), {
  'DESCRIPTOR' : _AUTHORIZATIONRESPONSE,
  '__module__' : 'spaceone.api.core.v1.handler_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.core.v1.AuthorizationResponse)
  })
_sym_db.RegisterMessage(AuthorizationResponse)

AuthenticationRequest = _reflection.GeneratedProtocolMessageType('AuthenticationRequest', (_message.Message,), {
  'DESCRIPTOR' : _AUTHENTICATIONREQUEST,
  '__module__' : 'spaceone.api.core.v1.handler_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.core.v1.AuthenticationRequest)
  })
_sym_db.RegisterMessage(AuthenticationRequest)

AuthenticationResponse = _reflection.GeneratedProtocolMessageType('AuthenticationResponse', (_message.Message,), {
  'DESCRIPTOR' : _AUTHENTICATIONRESPONSE,
  '__module__' : 'spaceone.api.core.v1.handler_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.core.v1.AuthenticationResponse)
  })
_sym_db.RegisterMessage(AuthenticationResponse)

EventRequest = _reflection.GeneratedProtocolMessageType('EventRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVENTREQUEST,
  '__module__' : 'spaceone.api.core.v1.handler_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.core.v1.EventRequest)
  })
_sym_db.RegisterMessage(EventRequest)


# @@protoc_insertion_point(module_scope)
