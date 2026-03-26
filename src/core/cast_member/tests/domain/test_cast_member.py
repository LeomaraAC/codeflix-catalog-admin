import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_name_and_type_is_required(self):
        with pytest.raises(TypeError, match='missing 2 required positional arguments: \'name\' and \'type\''):
            CastMember()

    def test_type_must_be_actor_or_director(self):
        with pytest.raises(ValueError, match='type must be either ACTOR or DIRECTOR'):
            CastMember(name='John Doe', type='WRITER')

    def test_name_must_have_less_than_255_characters(self):
        long_name = 'a' * 256
        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            CastMember(name=long_name, type=CastMemberType.ACTOR)

    def test_cast_member_is_created_with_provided_values(self):
        cast_member = CastMember(name='John Doe', type=CastMemberType.ACTOR)

        assert cast_member.name == 'John Doe'
        assert cast_member.type == CastMemberType.ACTOR

class TestUpdateCastMember:
    def test_update_cast_member_with_name_and_type(self):
        new_name = 'John Doe'
        type = CastMemberType.ACTOR
        cast_member = CastMember(name='Marie Doe', type=CastMemberType.DIRECTOR)
        cast_member.update_cast_member(name=new_name, type=type)

        assert cast_member.name == new_name
        assert cast_member.type == type

    def test_update_cast_member_with_invalid_type(self):
        cast_member = CastMember(name='Marie Doe', type=CastMemberType.DIRECTOR)

        with pytest.raises(ValueError, match='type must be either ACTOR or DIRECTOR'):
            cast_member.update_cast_member(name='John Doe', type='WRITER')

    def test_update_cast_member_with_invalid_name(self):
        new_name = 'John Doe' * 200
        cast_member = CastMember(name='Marie Doe', type=CastMemberType.DIRECTOR)

        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            cast_member.update_cast_member(name=new_name, type=CastMemberType.ACTOR)

    def test_update_cast_member_with_empty_name(self):
        cast_member = CastMember(name='John Doe', type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match='name cannot be empty'):
            cast_member.update_cast_member(name="", type=CastMemberType.ACTOR)