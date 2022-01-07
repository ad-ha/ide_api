# ide_api

Iberdrola Distribución (i-DE) Home Assistant Custom Integration

## Description

Adds integration with i-DE in Home Assistant

This sensor will update every hour.

Important: Keep in mind that each reading is done directly to your home meter, and it takes sometime to return a result. As per i-DE it may take up to 2 minutes to get a reading.

## Getting Started

### Dependencies

You should have an i-DE username and access to the Clients' website. You may register here: [Área Clientes | I-DE - Grupo Iberdrola](https://www.i-de.es/consumidores/web/guest/login).

Make sure to complement all information to have an "Advanced User" profile.

### Manual method

- Download/clone this repo
- Copy the [custom_components/ide_api](custom_components/ide_api) folder into your custom_components folder into your HA installation
- Restart HA

### [HACS](https://hacs.xyz/) method (recommended)

- Copy this repo URL
- In the HACS section, add this repo as a custom one:

  ![Custom repository](static/images/add_hacs_custom_repo.png)
  
  - On the "Repository" field put the URL copied before
  - On the "Catgory" select "Integration"
- Restart HA

## How to configure

- Edit your `configuration.yaml` (or your `sensor.yaml` without _`sensor:`_) file to add this sensor:

```yaml
sensor:
  - platform: ide
    username: <username>
    password: <password>
```

Use the _\<username\>_ and _\<password\>_ you use on the i-DE webpage. (It is recommended to use the [HA secrets](https://www.home-assistant.io/docs/configuration/secrets/) files for security pourposes)

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

In the `sensor.yaml` file or under sensor in `configuration.yaml`

- With the cost calculations template (inside your `configuration.yaml` file) as:

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

![Toll p1](static/images/helpers_toll_p1.png)
![Power p1](static/images/helpers_power_p1.png)

Once created, you can define the amounts in the box that appears in the details of each input_number or in Developer Tools / States

## Authors

- [Alvaro Duarte](https://github.com/ad-ha)  

### Contributions

- [alessbarb](https://github.com/alessbarb)
- [NeoMorfeo](https://github.com/NeoMorfeo)

## Version History

```
0.0.3
- Update version number to 0.0.3
```
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

THIS PROJECT IS NOT IN ANY WAY ASSOCIATED WITH OR RELATED TO THE IBERDROLA GROUP COMPANIES OR ANY OTHER. The information here and online is for educational and resource purposes only and therefore the developers do not endorse or condone any inappropriate use of it, and take no legal responsibility for the functionality or security of your devices.

