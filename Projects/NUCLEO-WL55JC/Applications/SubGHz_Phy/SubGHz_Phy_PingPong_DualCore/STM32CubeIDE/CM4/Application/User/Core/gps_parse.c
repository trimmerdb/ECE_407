/*
 * rmc_parse.c
 *
 *  Created on: Feb 25, 2026
 *      Author: my1du
 */


#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "gps_parse.h"
#include "sys_app.h"

#define NMEA_LINE_SIZE 128

static uint16_t last_pos = 0;              // last processed index in DMA buffer
static uint8_t nmea_line_buffer[NMEA_LINE_SIZE];
static uint16_t nmea_index = 0;


extern GPS_Data_t gps_data;
extern uint8_t uart_rx_byte;
extern uint8_t uart_rx_buffer[UART_BUFFER_SIZE];
extern UART_HandleTypeDef huart1;

int GPS_Parse_RMC(char *nmea, GPS_Data_t *gps)
{
	if (strstr(nmea, "RMC") == NULL)
	    return 0;

    char *token;
    int field = 0;

    char *lat_str = NULL;
    char *lat_dir = NULL;
    char *lon_str = NULL;
    char *lon_dir = NULL;
    char *speed_str = NULL;

    token = strtok(nmea, ",");

    while (token != NULL)
    {
        switch (field)
        {
            case 2: // Status
                if (token[0] != 'A'){
                    return 0; // Invalid fix
                }
                gps->valid = 1;
                break;

            case 3:
                lat_str = token;
                break;

            case 4:
                lat_dir = token;
                break;

            case 5:
                lon_str = token;
                break;

            case 6:
                lon_dir = token;
                break;

            case 7:
                speed_str = token;
                break;
        }

        token = strtok(NULL, ",");
        field++;
    }

    if (!lat_str || !lon_str || !speed_str)
        return 0;

    // Convert latitude
    float lat_raw = atof(lat_str);
    int lat_deg = (int)(lat_raw / 100);
    float lat_min = lat_raw - (lat_deg * 100);
    gps->latitude = lat_deg + (lat_min / 60.0f);

    if (lat_dir[0] == 'S')
        gps->latitude *= -1;

    // Convert longitude
    float lon_raw = atof(lon_str);
    int lon_deg = (int)(lon_raw / 100);
    float lon_min = lon_raw - (lon_deg * 100);
    gps->longitude = lon_deg + (lon_min / 60.0f);

    if (lon_dir[0] == 'W')
        gps->longitude *= -1;

    // Speed (knots)
    gps->speed_knots = atof(speed_str);

    return 1;
}

int GPS_Parse_GGA(char *nmea, GPS_Data_t *gps)
{
    if (strstr(nmea, "GGA") == NULL)
        return 0;

    char *token;
    int field = 0;

    char *lat_str = NULL;
    char *lat_dir = NULL;
    char *lon_str = NULL;
    char *lon_dir = NULL;
    char *fix_str = NULL;
    char *alt_str = NULL;

    token = strtok(nmea, ",");

    while (token != NULL)
    {
        switch (field)
        {
            case 2: // Latitude
                lat_str = token;
                break;

            case 3: // N/S
                lat_dir = token;
                break;

            case 4: // Longitude
                lon_str = token;
                break;

            case 5: // E/W
                lon_dir = token;
                break;

            case 6: // Fix Quality
                fix_str = token;
                break;

            case 9: // Altitude
                alt_str = token;
                break;
        }

        token = strtok(NULL, ",");
        field++;
    }

    if (!lat_str || !lon_str || !fix_str || !alt_str)
        return 0;

    // Fix quality
    gps->fix = (uint8_t)atoi(fix_str);

    gps->valid = 1;

    // Convert latitude
    float lat_raw = atof(lat_str);
    int lat_deg = (int)(lat_raw / 100);
    float lat_min = lat_raw - (lat_deg * 100);
    gps->latitude = lat_deg + (lat_min / 60.0f);

    if (lat_dir && lat_dir[0] == 'S')
        gps->latitude *= -1;

    // Convert longitude
    float lon_raw = atof(lon_str);
    int lon_deg = (int)(lon_raw / 100);
    float lon_min = lon_raw - (lon_deg * 100);
    gps->longitude = lon_deg + (lon_min / 60.0f);

    if (lon_dir && lon_dir[0] == 'W')
        gps->longitude *= -1;

    // Altitude (meters)
    gps->altitude = atof(alt_str);

    if (gps->fix == 0)
    {
        gps->valid = 0;
        return 0;  // No fix
    }

    return 1;
}

void ParseGpsData(void)
{
    // Get current DMA write position
    uint16_t dma_pos = UART_BUFFER_SIZE - __HAL_DMA_GET_COUNTER(huart1.hdmarx);

    // Process all new bytes
    while (last_pos != dma_pos)
    {
        uint8_t byte = uart_rx_buffer[last_pos];

        // Store in NMEA line buffer
        if (nmea_index < NMEA_LINE_SIZE - 1)
            nmea_line_buffer[nmea_index++] = byte;

        // Check for end of NMEA sentence
        if (byte == '\n')
        {
            nmea_line_buffer[nmea_index] = '\0'; // null-terminate

            if (GPS_Parse_GGA((char*)nmea_line_buffer, &gps_data))
            {
                // gps_data now contains valid latitude, longitude, speed
                char logBuffer[128];
                sprintf(logBuffer,
                        "GPS Parsed: Lat %.7f Lon %.7f Speed %.2f\r\n",
                        gps_data.latitude, gps_data.longitude, gps_data.speed_knots);
                APP_LOG(TS_ON, VLEVEL_L, "%s", logBuffer);
            }

            nmea_index = 0; // reset for next sentence
        }

        // Advance last_pos with wrap-around
        last_pos++;
        if (last_pos >= UART_BUFFER_SIZE)
            last_pos = 0;
    }
}
