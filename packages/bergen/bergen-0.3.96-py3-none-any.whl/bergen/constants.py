
from bergen.queries.delayed.node import DETAIL_NODE_FR
from bergen.schema import Assignation, Node, Peasent, Template, Pod, Provision, Transcript, VartPod, Volunteer
from bergen.query import TypedGQL


NEGOTIATION_GQL = TypedGQL("""

  mutation Negotiate($clientType: ClientTypeInput!) {
  negotiate(clientType: $clientType) {
    timestamp
    extensions
    models {
        identifier
        point {
            id
            outward
            port
            type
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

 
# Peasent Constants

SERVE_GQL = TypedGQL("""
    mutation Serve($name: String!){
        serve(name: $name){
            id
            name
            
        }
    }
""", Peasent)



OFFER_GQL = TypedGQL("""
    mutation Offer($node: ID!, $params: GenericScalar!, $policy: GenericScalar!){
        offer(node: $node, params: $params, policy: $policy){
            id
            name
            policy 
        }
    }
""", Template)


ACCEPT_GQL = TypedGQL("""
    mutation Accept($template: ID!, $provision: String!){
        accept(template: $template, provision: $provision){
            id
            template {
                node {"""
                + DETAIL_NODE_FR +
                """

                }
            }
        }
    }
""", Pod)




PROVIDE_GQL = TypedGQL("""
        subscription Provide($reference: String!, $node: ID!, $selector: SelectorInput!){
            provide(node: $node , selector: $selector, reference: $reference){
                pod {
                    id
                    status
                }
                node {
                    name
                }
                reference
                status
                statusmessage

            }
        }      
    """, Provision)



ASSIGN_GQL = TypedGQL("""
        subscription Assignation($inputs: GenericScalar!, $pod: ID!, $reference: String!) {
            assign(inputs: $inputs, pod: $pod, reference: $reference){
                inputs
                outputs
                status
                statusmessage
            }
        }     
""", Assignation)