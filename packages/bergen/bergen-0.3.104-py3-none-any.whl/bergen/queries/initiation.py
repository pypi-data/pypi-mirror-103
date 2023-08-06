from bergen.schema import Assignation, DataModel, Node, Peasent, Template, Pod, Provision, Transcript, VartPod, Volunteer
from bergen.query import TypedGQL


NEGOTIATION_GQL = TypedGQL("""

  mutation Negotiate(
      $clientType: ClientTypeInput!
      $inward: String,
      $outward: String,
      $port: Int,
      $version: String,
      $pointType: DataPointTypeInput,
      $needsNegotiation: Boolean
      
      ) {
  negotiate(
      clientType: $clientType,
      inward: $inward,
      outward: $outward,
      port: $port,
      version: $version,
      pointType: $pointType,
      needsNegotiation: $needsNegotiation
  ) {
    timestamp
    extensions
    models {
        identifier
        point {
            id
            outward
            port
            type
            needsNegotiation
        }
    }
    postman {
        type
        kwargs
    }
    provider {
        type
        kwargs
    }
    host {
        type
        kwargs
    }
  }
  }
""", Transcript)


HOST_GQL = TypedGQL("""
    mutation Host($identifier: String!, $extenders: [String]){
        host(identifier: $identifier, extenders: $extenders){
            id
            identifier
            extenders
            point {
                inward
            }
        }
    }
""", DataModel)