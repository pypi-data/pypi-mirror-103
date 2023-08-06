{% load django_ts_bridge %}
{% for app_key, app in choices.items  %}
    {% for model_key, model in app.items  %}
        {% for choice_definition_key, choice_definition in model.items %}
            enum {{app_key}}{{model_key}}{{choice_definition_key}} {
                {% for choice_key, choice in choice_definition.items %}
                    {{choice_key}} = {{choice|js_literal|safe}},
                {% endfor %}
            }
        {% endfor %}
    {% endfor %}
{% endfor %}
export class {{ ts_var_name }} {
    {% for app_key, app in choices.items %}
        static readonly {{app_key}} = class {
            {% for model_key, model in app.items %}
                static readonly {{model_key}} = class {
                    {% for choice_key, choice_definition in model.items %}
                        static readonly {{choice_key}} = {{app_key}}{{model_key}}{{choice_key}};
                    {% endfor %}
                }
            {% endfor %}
        }
    {% endfor %}
}