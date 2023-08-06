{{ fullname | escape | underline }}

{% block modules %}
{% if modules %}
.. autosummary::
   :toctree:
   :shorttoc:
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

.. automodule:: {{ fullname }}

   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :toctree:
      :shorttoc:
      :nosignatures:

      .. raw:: latex

         \iffalse

   {% for item in classes %}
      {{ item }}
   {%- endfor %}

      .. raw:: latex

         \fi

   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
      :toctree:
      :shorttoc:
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
      :toctree:
      :shorttoc:
      :nosignatures:
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if all_attributes %}
   .. rubric:: Module attributes

   .. currentmodule:: {{ fullname }}
   {% for item in all_attributes %}
   .. autodata:: {{ item }}
   {% endfor %}
   {% endif %}
   {% endblock %}

