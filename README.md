# ide_api

Iberdrola Distribución (i-DE) Home Assistant Custom Integration

## Description

Adds integration with i-DE in Home Assistant

## Getting Started

### Dependencies

You should be registered in i-DE, if not you can register here: [Área Clientes | I-DE - Grupo Iberdrola](https://www.i-de.es/consumidores/web/guest/login).

### Installing

- Copy the contents of `custom_components/ide_api/` to `<your config dir>/custom_components/ide_api/`.
- Restart Home Assistant
- Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: ide
    username: YOUR_USERNAME
    password: YOUR_PASSWORD
```

- Restart Home Assistant again.

### Usage

#### Sensors

Utility Meter sensors inside configuration.yaml
```yaml
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

In the sensor.yaml file or under sensor in configuration.yaml

```yaml
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

To complement the cost calculation, I consider the costs of Toll, Energy Tax and VAT. For that create some "helpers" with input_number.

* input_number.impuesto_energia (%) >> 1.051127
* input_number.iva_energia (%) >> 1.10
* input_number.peaje_energia_p1 (this what you have in the invoice)
* input_number.peaje_energia_p2 (this what you have in the invoice)
* input_number.peaje_energia_p3 (this what you have in the invoice)
* input_number.peaje_energia_potencia_p1 (this what you have in the invoice)
* input_number.peaje_energia_potencia_p2 (this what you have in the invoice)

Once created, you can define the amounts in the box that appears in the details of each input_number or in Developer Tools / States

## Authors

- [Alvaro Duarte](https://github.com/ad-ha)  

## Version History

```
0.0.3a - Debug log Update and Security Fix
- Fix debug log target file, causing performance issues on HA
- Fix security issue, where login details to IDE where stored as plain text on the log file
- Update versioning across all files
- Update HACS release
```
```
0.0.2
- Removed b from versioning
```
```
0.0.1b - Initial Beta release
- Beta Release of iDE Energy Monitor Custom Integration for Home Assistant
```

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE file for details

## Disclaimer

THIS PROJECT IS NOT IN ANY WAY ASSOCIATED WITH OR RELATED TO THE IBERDROLA GROUP COMPANIES OR ANY OTHER. The information here and online is for educational and resource purposes only and therefore the developers do not endorse or condone any inappropriate use of it, and take no legal responsibility for the functionality or security of your alarms and devices.
