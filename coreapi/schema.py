BIOMIO_protocol_json_schema = {
    "title": "Biomio Schema",
    "id": "http://biom.io/entry-schema#",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "schema of BIOMIO communication protocol",
    "type": "object",
    "required": ["header", "msg"],
    "properties": {
        "header": {
            "oneOf": [
                {"$ref": "#/definitions/serverHeader"},
                {"$ref": "#/definitions/clientHeader"}
            ]
        },
        "msg": {
            "oneOf": [
                {"$ref": "#/definitions/bye"},
                {"$ref": "#/definitions/ack"},
                {"$ref": "#/definitions/nop"},
                {"$ref": "#/definitions/clientHello"},
                {"$ref": "#/definitions/resources"},
                {"$ref": "#/definitions/again"},
                {"$ref": "#/definitions/auth"},
                {"$ref": "#/definitions/probe"},
                {"$ref": "#/definitions/verify"},
                {"$ref": "#/definitions/identify"},
                {"$ref": "#/definitions/rpcReq"},
                {"$ref": "#/definitions/rpcResp"},
                {"$ref": "#/definitions/rpcEnumNsReq"},
                {"$ref": "#/definitions/rpcEnumNsResp"},
                {"$ref": "#/definitions/rpcEnumCallsReq"},
                {"$ref": "#/definitions/rpcEnumCallsResp"},
                {"$ref": "#/definitions/serverHello"},
                {"$ref": "#/definitions/try"},
                {"$ref": "#/definitions/data"},
                {"$ref": "#/definitions/getResources"}
            ]
        },
        "status": { "type": "string" }
    },
    "definitions": {
        "nop": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["nop"] }
            }
        },
        "ack": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["ack"] }
            }
        },
        "bye": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["bye"] }
            }
        },
        "getResources": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["getResources"] }
            }
        },
        "policy": {
            "type": "object",
            "properties": {
                "condition": {"enum": ["none", "all", "any"]}
            }
        },
        "resource": {
            "type": "object",
            "required": ["rType", "rProperties"],
            "properties": {
                "rType": {"enum": ["fp-scanner", "mic", "front-cam", "back-cam", "input",
                                   "ldap_connection", "location", "interact", "db_connection"]},
                "rProperties": {"type": "string"}
            }
        },
        "resourceItem": {
            "type": "object",
            "required": ["tType", "resource", "samples"],
            "properties": {
                "tType": {"enum": ["fp", "face", "palm", "voice", "ldap_check", "text_input", "location",
                                   "push_button", "pin_code", "credit_card"]},
                "resource": {"$ref": "#/definitions/resource"},
                "samples": {"type": "number"}
            }
        },
        "serverHeader": {
            "type": "object",
            "name": "serverHeader",
            "required": ["oid","seq", "protoVer", "token"],
            "properties": {
                "oid": { "enum": ["serverHeader"] },
                "seq": {"type": "number"},
                "protoVer": {"type": "string"},
                "token": {"type": "string"}
            }
        },
        "serverHello": {
            "type": "object",
            "required": ["oid", "refreshToken", "sessionttl", "connectionttl"],
            "properties": {
                "oid": { "enum": ["serverHello"] },
                "refreshToken": {"type": "string"},
                "sessionttl": {"type": "number"},
                "connectionttl": {"type": "number"},
                "key": {"type": "string"},
                "fingerprint": {"type": "string"}
            }
        },
        "try": {
            "type": "object",
            "oneOf": [
                {"$ref": "#/definitions/tryMessageString"},
                {"$ref": "#/definitions/tryMessageArray"}
            ]
        },
        "tryMessageArray": {
            "type": "object",
            "required": ["oid", "resource", "authTimeout"],
            "properties": {
                "oid": { "enum": ["try"] },
                "try_id": {"type": "string"},
                "authTimeout": {"type": "number"},
                "policy": {"$ref": "#/definitions/policy"},
                "try_info": {"type": "string"},
                "resource": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/resourceItem"}
                },
                "message": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "tryMessageString": {
            "type": "object",
            "required": ["oid", "resource", "authTimeout"],
            "properties": {
                "oid": { "enum": ["try"] },
                "try_id": {"type": "string"},
                "authTimeout": {"type": "number"},
                "policy": {"$ref": "#/definitions/policy"},
                "try_info": {"type": "string"},
                "resource": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/resourceItem"}
                },
                "message": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "data": {
            "type": "object",
            "required": ["keys", "values"],
            "properties": {
            "oid": { "enum": ["data"] },
                "keys": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "values": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "clientHeader": {
            "type": "object",
            "required": ["oid", "seq", "protoVer", "osId", "appType"],
            "properties": {
                "oid": { "enum": ["clientHeader"] },
                "seq": {"type": "number"},
                "protoVer": {"type": "string"},
                "appId": {"type": "string"},
                "appType": {"type": "string"},
                "osId": {"type": "string"},
                "devId": {"type": "string"},
                "token": {"type": "string"}
            }
        },
        "clientHello": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["clientHello"] },
                "secret": {"type": "string"},
                "apnsToken": {"type": "string"},
            }
        },
        "auth": {
            "type": "object",
            "required": ["oid", "key"],
            "properties": {
                "oid": { "enum": ["auth"] },
                "key": { "type": "string" }
            }
        },
        "again": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["again"] }
            }
        },
        "resources": {
            "type": "object",
            "required": ["oid", "data"],
            "properties": {
                "oid": { "enum": ["resources"] },
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/resource"}
                },
                "push_token": {"type": "string"}
            }
        },
        "imageSamples": {
            "type": "object",
            "required": ["oid", "samples"],
            "properties": {
                "oid": { "enum": ["imageSamples"] },
                "samples": {
                    "type": "array",
                    "items": {
                        "media": {
                            "type": "image/png",
                            "binaryEncoding": "base64"
                        },
                        "type": "string"
                    }
                }
            }
        },
        "soundSamples": {
            "type": "object",
            "required": ["oid", "samples"],
            "properties": {
                "oid": { "enum": ["soundSamples"] },
                "samples": {
                    "type": "array",
                    "items": {
                        "media": {
                            "type": "image/png",
                            "binaryEncoding": "base64"
                        },
                        "type": "string"
                    }
                }
            }
        },
        "touchIdSamples": {
            "type": "object",
            "required": ["oid", "samples"],
            "properties": {
                "oid": { "enum": ["touchIdSamples"] },
                "samples": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "locationSamples": {
            "type": "object",
            "required": ["oid", "samples"],
            "properties": {
                "oid": { "enum": ["locationSamples"] },
                "samples": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "pushbuttonSamples": {
            "type": "object",
            "required": ["oid", "samples"],
            "properties": {
                "oid": { "enum": ["pushbuttonSamples"] },
                "samples": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        "pincodeSamples": {
            "type": "object",
            "required": ["oid", "samples"],
            "properties": {
                "oid": { "enum": ["pincodeSamples"] },
                "samples": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        },
        # TODO: improve in future - separate messages to send each photo
        "probe": {
            "type": "object",
            "required": ["oid", "probeStatus"],
            "properties": {
                "oid": { "enum": ["probe"] },
                "try_id": {"type": "string"},
                "tType": {"type": "string"},
                "probeData": {
                    "oneOf": [
                        {"$ref": "#/definitions/imageSamples"},
                        {"$ref": "#/definitions/soundSamples"},
                        {"$ref": "#/definitions/touchIdSamples"},
                        {"$ref": "#/definitions/locationSamples"},
                        {"$ref": "#/definitions/pushbuttonSamples"},
                        {"$ref": "#/definitions/pincodeSamples"}
                    ]
                },
                "probeStatus": { "enum": ["success", "failed", "canceled", "received"] }
            }
        },
        "verify": {
            "type": "object",
            "required": ["oid", "id"],
            "properties": {
                "oid": { "enum": ["verify"] },
                "id": {"type": "string"}
            }
        },
        "identify": {
            "type": "object",
            "required": ["oid"],
            "properties": {
            "oid": { "enum": ["identify"] }
            }
        },
        "rpcData": {
            "type": "object",
            "required": ["keys", "values"],
            "properties": {
                "keys": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "values": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "rpcEnumNsReq": {
            "type": "object",
            "required": ["oid"],
            "properties": {
                "oid": { "enum": ["rpcEnumNsReq"] }
            }
        },
        "rpcEnumNsResp": {
            "type": "object",
            "required": ["oid", "namespaces"],
            "properties": {
                "oid": { "enum": ["rpcEnumNsResp"] },
                "namespaces": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "rpcEnumCallsReq": {
            "type": "object",
            "required": ["oid", "ns"],
            "properties": {
                "oid": { "enum": ["rpcEnumNsReq"] },
                "ns": {"type": "string"}
            }
        },
        "rpcEnumCallsResp": {
            "type": "object",
            "required": ["oid", "calls"],
            "properties": {
                "oid": { "enum": ["rpcEnumCallsResp"] },
                "calls": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "params": {
                    "type": "array",
                    "items": {"type": "string"}
                    # fixed to make fysom works
                    # {
                    #     "type": "array",
                    #     "items": {"type": "string"}
                    # }
                }
            }
        },
        "rpcReq": {
            "type": "object",
            "required": ["oid", "namespace", "call"],
            "properties": {
                "oid": { "enum": ["rpcReq"] },
                "session_id": {"type": "string"},
                "onBehalfOf": {"type": "string"},
                "namespace": {"type": "string"},
                "call": {"type": "string"},
                "data": {"$ref": "#/definitions/rpcData"}
            }
        },
        "rpcResp": {
            "type": "object",
            "required": ["oid", "namespace", "call", "data"],
            "properties": {
                "oid": { "enum": ["rpcResp"] },
                "session_id": {"type": "string"},
                "onBehalfOf": {"type": "string"},
                "namespace": {"type": "string"},
                "call": {"type": "string"},
                "data": {"$ref": "#/definitions/rpcData"},
                "rpcStatus": {"enum": ["complete", "inprogress", "fail"]}
            }
        },
        "rect": {
            "type": "object",
            "required": ["x", "y", "width", "height"],
            "properties": {
                "x": {"type": "number"},
                "y": {"type": "number"},
                "height": {"type": "number"},
                "width": {"type": "number"}
            }
        },
        "detected": {
            "type": "object",
            "required": ["oid", "rects"],
            "properties": {
            "oid": { "enum": ["detected"] },
                "distance": {"type": "number"},
                "rects": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/rect"}
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    }
}
