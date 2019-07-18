import graphene
import graphene_jwt
import backend.main.schema


class Query(
    backend.main.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    backend.main.schema.Mutation,
    graphene.ObjectType
):
    token_auth = graphene_jwt.ObtainJSONWebToken.Field()
    verify_token = graphene_jwt.Verify.Field()
    refresh_token = graphene_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
