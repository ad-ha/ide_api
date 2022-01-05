# ie_api

i-DE Home Assistant Custom Integration

This sensor will update every 2 hours.

## How to install

### Manual method

- Download/clone this repo
- Copy the [custom_components/ide_api](custom_components/ide_api) folder into your custom_components folder into your HA installation
- Restart HA

### [HACS](https://hacs.xyz/) method

- Copy this repo URL
- In the HACS section, add this repo as a custom one:
  ![Custom repository](static/images/add_hacs_custom_repo.png)
  - On the "Repository" field put the URL copied before
  - On the "Catgory" select "Integration"
- Restart HA

## How to configure

- Edit your `configuration.yaml` (or your `sensor.yaml` without _`sensor:`_) file to add this sensor:

```yml
sensor:
  - platform: ide
    username: <username>
    password: <password>
```

use the _\<username\>_ and _\<password\>_ you use on the i-de webpage. (It is recommended to use the [HA secrets](https://www.home-assistant.io/docs/configuration/secrets/) files for security pourposes)

- Restart HA

## How to configure hourly, daily and monthly costs sensors

- Edit your `configuration.yaml` file to add this sensor:

```yml
# UTILITY METER #
utility_meter:
  # HOME ENERGY #
  home_energy_hourly:
    source: sensor.ide_meter_reading
    cycle: hourly

  home_energy_daily:
    source: sensor.ide_meter_reading
    cycle: daily

  home_energy_monthly:
    source: sensor.ide_meter_reading
    cycle: monthly

  home_energy_cost_hourly:
    source: sensor.home_energy_cost
    cycle: hourly

  home_energy_cost_daily:
    source: sensor.home_energy_cost
    cycle: daily

  home_energy_cost_monthly:
    source: sensor.home_energy_cost
    cycle: monthly
```

- With the cost calculations template (inside your `configuration.yaml` file) as:

```yml
# ENERGY COST #
- platform: template
  sensors:
    home_energy_cost:
      friendly_name: "Home Energy Cost"
      unit_of_measurement: "€"
      value_template: >
        {% if is_state_attr('sensor.pvpc', 'period', 'P1') %} {% set peaje=states('input_number.peaje_energia_p1') | float %}
        {% elif is_state_attr('sensor.pvpc', 'period', 'P2') %} {% set peaje=states('input_number.peaje_energia_p2') | float %}
        {% elif is_state_attr('sensor.pvpc', 'period', 'P3') %} {% set peaje=states('input_number.peaje_energia_p3') | float %}
        {% endif %}
        {{ (( states('sensor.home_energy_hourly') | float * (peaje + states('sensor.pvpc') | float) ) * states('input_number.impuesto_energia') | float * states('input_number.iva_energia') | float) | round(3) }}
```

- Create some helpers to configure the costs:

```
input_number.impuesto_energia (%) >> 1.051127
input_number.iva_energia (%) >> 1.10
input_number.peaje_energia_p1 (esto lo que tengáis de vuestra comercializadora en la factura)
input_number.peaje_energia_p2 (esto lo que tengáis de vuestra comercializadora en la factura)
input_number.peaje_energia_p3 (esto lo que tengáis de vuestra comercializadora en la factura)
input_number.peaje_energia_potencia_p1 (esto lo que tengáis de vuestra comercializadora en la factura)
input_number.peaje_energia_potencia_p2 (esto lo que tengáis de vuestra comercializadora en la factura)
```

![Toll p1](static/images/helpers_toll_p1.png)
![Power p1](static/images/helpers_power_p1.png)
