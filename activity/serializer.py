
from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'category', 'type', 'description', 'carbon_emission_kg', 'date']
        read_only_fields = ['user', 'carbon_emission_kg', 'date']

    def validate(self, attrs):
        category = attrs.get('category')
        type_ = attrs.get('type')

        valid_types = {
            'transport': ['car', 'bike', 'bus'],
            'diet': ['veg', 'non_veg', 'vegan'],
            'energy': ['appliances', 'lighting', 'heating']
        }

        if type_ and type_ not in valid_types.get(category, []):
            raise serializers.ValidationError({
                'type': f"Invalid type '{type_}' for category '{category}'. Valid options: {valid_types.get(category)}"
            })

        return attrs

    def create(self, validated_data):
        category = validated_data['category']
        type_ = validated_data.get('type')

        emission_factors = {
            'transport': {'car': 5.0, 'bike': 0.5, 'bus': 1.5},
            'diet': {'veg': 1.0, 'non_veg': 3.0, 'vegan': 0.8},
            'energy': {'appliances': 2.0, 'lighting': 0.5, 'heating': 3.0}
        }

        # Auto-calculate emission
        validated_data['carbon_emission_kg'] = emission_factors.get(category, {}).get(type_, 0)

        # Assign the user automatically
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)