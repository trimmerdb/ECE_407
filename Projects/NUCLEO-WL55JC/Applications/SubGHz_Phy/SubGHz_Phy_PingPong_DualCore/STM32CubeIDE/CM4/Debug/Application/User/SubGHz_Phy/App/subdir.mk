################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/my1du/Repos/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/CM4/SubGHz_Phy/App/app_subghz_phy.c \
C:/Users/my1du/Repos/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/CM4/SubGHz_Phy/App/subghz_phy_app.c 

OBJS += \
./Application/User/SubGHz_Phy/App/app_subghz_phy.o \
./Application/User/SubGHz_Phy/App/subghz_phy_app.o 

C_DEPS += \
./Application/User/SubGHz_Phy/App/app_subghz_phy.d \
./Application/User/SubGHz_Phy/App/subghz_phy_app.d 


# Each subdirectory must supply rules for building sources it contributes
Application/User/SubGHz_Phy/App/app_subghz_phy.o: C:/Users/my1du/Repos/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/CM4/SubGHz_Phy/App/app_subghz_phy.c Application/User/SubGHz_Phy/App/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DCORE_CM4 -DUSE_HAL_DRIVER -DSTM32WL55xx -c -I../../../CM4/Core/Inc -I../../../CM4/SubGHz_Phy/App -I../../../CM4/MbMux -I../../../Common/Board -I../../../Common/System -I../../../Common/MbMux -I../../../../../../../../Drivers/BSP/STM32WLxx_Nucleo -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc/Legacy -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32WLxx/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Drivers/CMSIS/Include -Og -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"
Application/User/SubGHz_Phy/App/subghz_phy_app.o: C:/Users/my1du/Repos/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/CM4/SubGHz_Phy/App/subghz_phy_app.c Application/User/SubGHz_Phy/App/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DCORE_CM4 -DUSE_HAL_DRIVER -DSTM32WL55xx -c -I../../../CM4/Core/Inc -I../../../CM4/SubGHz_Phy/App -I../../../CM4/MbMux -I../../../Common/Board -I../../../Common/System -I../../../Common/MbMux -I../../../../../../../../Drivers/BSP/STM32WLxx_Nucleo -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc/Legacy -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32WLxx/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Drivers/CMSIS/Include -Og -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Application-2f-User-2f-SubGHz_Phy-2f-App

clean-Application-2f-User-2f-SubGHz_Phy-2f-App:
	-$(RM) ./Application/User/SubGHz_Phy/App/app_subghz_phy.cyclo ./Application/User/SubGHz_Phy/App/app_subghz_phy.d ./Application/User/SubGHz_Phy/App/app_subghz_phy.o ./Application/User/SubGHz_Phy/App/app_subghz_phy.su ./Application/User/SubGHz_Phy/App/subghz_phy_app.cyclo ./Application/User/SubGHz_Phy/App/subghz_phy_app.d ./Application/User/SubGHz_Phy/App/subghz_phy_app.o ./Application/User/SubGHz_Phy/App/subghz_phy_app.su

.PHONY: clean-Application-2f-User-2f-SubGHz_Phy-2f-App

