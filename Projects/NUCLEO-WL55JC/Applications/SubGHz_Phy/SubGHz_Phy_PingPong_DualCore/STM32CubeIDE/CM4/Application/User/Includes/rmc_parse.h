/*
 * rmc_parse.h
 *
 *  Created on: Feb 25, 2026
 *      Author: my1du
 */

#ifndef APPLICATION_USER_INCLUDES_RMC_PARSE_H_
#define APPLICATION_USER_INCLUDES_RMC_PARSE_H_

#include "main.h"

typedef struct
{
  float latitude;
  float longitude;
  float speed_knots;
  uint8_t valid;
} GPS_Data_t;

int GPS_Parse_RMC(char *nmea, GPS_Data_t *gps);

void ParseGpsData(void);

#endif /* APPLICATION_USER_INCLUDES_RMC_PARSE_H_ */
