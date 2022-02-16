# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tags.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tags.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\ntags.proto\"\x1c\n\x0cImageRequest\x12\x0c\n\x04\x66ile\x18\x01 \x01(\x0c\"\x19\n\tTagsReply\x12\x0c\n\x04tags\x18\x01 \x03(\t2.\n\x04Tags\x12&\n\x07getTags\x12\r.ImageRequest\x1a\n.TagsReply\"\x00\x62\x06proto3'
)




_IMAGEREQUEST = _descriptor.Descriptor(
  name='ImageRequest',
  full_name='ImageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file', full_name='ImageRequest.file', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=14,
  serialized_end=42,
)


_TAGSREPLY = _descriptor.Descriptor(
  name='TagsReply',
  full_name='TagsReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tags', full_name='TagsReply.tags', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=44,
  serialized_end=69,
)

DESCRIPTOR.message_types_by_name['ImageRequest'] = _IMAGEREQUEST
DESCRIPTOR.message_types_by_name['TagsReply'] = _TAGSREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ImageRequest = _reflection.GeneratedProtocolMessageType('ImageRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEREQUEST,
  '__module__' : 'tags_pb2'
  # @@protoc_insertion_point(class_scope:ImageRequest)
  })
_sym_db.RegisterMessage(ImageRequest)

TagsReply = _reflection.GeneratedProtocolMessageType('TagsReply', (_message.Message,), {
  'DESCRIPTOR' : _TAGSREPLY,
  '__module__' : 'tags_pb2'
  # @@protoc_insertion_point(class_scope:TagsReply)
  })
_sym_db.RegisterMessage(TagsReply)



_TAGS = _descriptor.ServiceDescriptor(
  name='Tags',
  full_name='Tags',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=71,
  serialized_end=117,
  methods=[
  _descriptor.MethodDescriptor(
    name='getTags',
    full_name='Tags.getTags',
    index=0,
    containing_service=None,
    input_type=_IMAGEREQUEST,
    output_type=_TAGSREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TAGS)

DESCRIPTOR.services_by_name['Tags'] = _TAGS

# @@protoc_insertion_point(module_scope)
