# Welcome to the dataoutsider visualization toolbox!

## Featuring
* pie_tree chart
 * level plot

## pie_tree
Need to display hierarchical density as pie-shaped areas?

1. Select [1 to n] categorical columns from a dataframe to group by 
1. Configure the chart ordering and hierarchy orientation
1. The pie_tree chart will create a hierarchical set of areas sized by the number of rows in each group at each level

### Example:
```
import dataoutsider as dr

df = dr.load_aircraft_df()
levels = ['Registrant', 'Aircraft', 'Engine', 'seats_bin']

inner_radius = 0.5
outer_radius = 2.0
starting_angle = 0.0
ending_angle = 360.0
point_resolution = 200
pie_tree_df = dr.pie_tree_calc(
    df, levels, 
    inner_radius, 
    outer_radius, 
    starting_angle, 
    ending_angle, 
    point_resolution)

dr.pie_tree_plot(pie_tree_df, 4)
```

![This is a alt text.](https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-domaincom-v1-0-0%2F690%2F492690%2FdYt43lIQ%2F35d90b39d7954382a1668e8272cc367e&methods=resize%2C600%2C5000 "pie_tree chart!")

### Variations:
```
inner_radius = 0.0
outer_radius = 2.0
```

![This is a alt text.](https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-domaincom-v1-0-0%2F690%2F492690%2FdYt43lIQ%2Fcf776778732f47549c4c98a05ebe8a04&methods=resize%2C600%2C5000 "inner_radius = 0.0")

```
starting_angle = 0.0
ending_angle = 90.0
```

![This is a alt text.](https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-domaincom-v1-0-0%2F690%2F492690%2FdYt43lIQ%2Fcaeccf46429a4949af6f208032dd8f2b&methods=resize%2C600%2C5000 "0-90 degrees")

### Extra Parameters:

| Parameter | Values | Description |
| :- | :- | :- |
| **default_sort** | True/False | Default: *False*, True: pandas sort, False: data sort |
| **default_sort_override** | True/False | Default: *True*, True: overrides default_sort |
| **default_sort_override_reversed** | True/False | Default: *False*, sort areas True: desc, False: asc |
| **all_vertical** | True/False | Default: *False*, True: break levels vertically, False: alternate |

### Plotting:

From the above example with 4 possible levels:

> Level 3 only

`dr.pie_tree_plot(pie_tree_df, 3)`

![This is a alt text.](https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-domaincom-v1-0-0%2F690%2F492690%2FdYt43lIQ%2F9bf4a0bc4091495da19862fe64631be8&methods=resize%2C600%2C5000 "Level 3 only")

> Level 2 **bold** outline
>> Level 3 thin outline

`dr.pie_tree_plot(pie_tree_df, 3)`

![This is a alt text.](https://images.builderservices.io/s/cdn/v1.0/i/m?url=https%3A%2F%2Fstorage.googleapis.com%2Fproduction-domaincom-v1-0-0%2F690%2F492690%2FdYt43lIQ%2F75b6b5bc77624eb29ee76ff352f24b46&methods=resize%2C600%2C5000 "Level 3, Level 2 bold")

### Tableau users:

#### Examples:

* Functional ideas (including mapping): [pie_tree](https://public.tableau.com/profile/nick.gerend#!/vizhome/pie_tree/pie_tree)
* Combined with a [Hierarchical Radial Tree Diagram]: [Takeoff](https://public.tableau.com/profile/nick.gerend#!/vizhome/Takeoff/Takeoff)

## Check back soon for updates!