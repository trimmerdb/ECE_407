################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/my1du/Repos/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/CM0PLUS/SubGHz_Phy/Target/radio_board_if.c 

OBJS += \
./Application/User/SubGHz_Phy/Target/radio_board_if.o 

C_DEPS += \
./Application/User/SubGHz_Phy/Target/radio_board_if.d 


# Each subdirectory must supply rules for building sources it contributes
Application/User/SubGHz_Phy/Target/radio_board_if.o: C:/Users/my1du/Repos/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/CM0PLUS/SubGHz_Phy/Target/radio_board_if.c Application/User/SubGHz_Phy/Target/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0plus -std=gnu11 -g3 -DDEBUG -DCORE_CM0PLUS -DUSE_HAL_DRIVER -DSTM32WL55xx -c -I../../../CM0PLUS/Core/Inc -I../../../CM0PLUS/SubGHz_Phy/App -I../../../CM0PLUS/SubGHz_Phy/Target -I../../../CM0PLUS/MbMux -I../../../Common/Board -I../../../Common/System -I../../../Common/MbMux -I../../../../../../../../Drivers/BSP/STM32WLxx_Nucleo -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc/Legacy -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32WLxx/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy/stm32_radio_driver -I../../../../../../../../Drivers/CMSIS/Include -Og -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Application-2f-User-2f-SubGHz_Phy-2f-Target

clean-Application-2f-User-2f-SubGHz_Phy-2f-Target:
	-$(RM) ./Application/User/SubGHz_Phy/Target/radio_board_if.cyclo ./Application/User/SubGHz_Phy/Target/radio_board_if.d ./Application/User/SubGHz_Phy/Target/radio_board_if.o ./Application/User/SubGHz_Phy/Target/radio_board_if.su

.PHONY: clean-Application-2f-User-2f-SubGHz_Phy-2f-Target

