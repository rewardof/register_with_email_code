from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Code


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password', 'placeholder': 'Password2'},
                                      write_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password2')
        read_only_fields = ('id', 'is_active')

    def save(self):
        user = User(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()
        return user


def code_interval(value):
    if not (value > 10000000 and value < 99999999):
        raise serializers.ValidationError('code must contains 8 numbers')


class CodeInterval:

    def __call__(self, value):
        if not (value > 10000000 and value < 99999999):
            raise serializers.ValidationError('code must contains 8 numbers')
        return value


class CodeSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(validators=[CodeInterval()])
    # code = serializers.IntegerField(validators=[code_interval])

    class Meta:
        model = Code
        fields = ('user', 'code')

    # def create(self, validated_data):
    #     code = validated_data.get('code')
    #     print(code)
    #     user = validated_data.pop('user')
    #     print(user)
    #     # user = User.objects.get(email=email)
    #     code_sent = int(self.context.get('code'))
    #     if code == code_sent:
    #         # code = Code.objects.create(user=user, code=code)
    #         code = super(CodeSerializer, self).create(**validated_data)
    #         user.is_active = True
    #         user.save()
    #         return code
    #     else:
    #         return serializers.ValidationError('Codes do not match')

    def create(self, validated_data):
        user = validated_data.get('user')
        # user = User.objects.get(email=user)
        code = validated_data.get('code')
        user.is_active = True
        user.save()
        return super(CodeSerializer, self).create(validated_data)

    def validate_code(self, value):
        code = value
        print(type(code))
        code_sent = self.context.get('code')
        print(type(code_sent))
        if code != code_sent:
            raise serializers.ValidationError('Codes do not match')
        else:
            return value
