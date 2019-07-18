import graphene
import graphene_jwt
from backend.main.schema import Query


class Mutation(
    graphene.ObjectType
):
    token_auth = graphene_jwt.ObtainJSONWebToken.Field()
    verify_token = graphene_jwt.Verify.Field()
    refresh_token = graphene_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
