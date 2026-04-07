################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Repositories/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/Common/System/sys_debug.c 

OBJS += \
./Application/User/Common/System/sys_debug.o 

C_DEPS += \
./Application/User/Common/System/sys_debug.d 


# Each subdirectory must supply rules for building sources it contributes
Application/User/Common/System/sys_debug.o: C:/Repositories/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/Common/System/sys_debug.c Application/User/Common/System/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DCORE_CM4 -DUSE_HAL_DRIVER -DSTM32WL55xx -c -I../../../CM4/Core/Inc -I../../../CM4/SubGHz_Phy/App -I../../../CM4/MbMux -I../../../Common/Board -I../../../Common/System -I../../../Common/MbMux -I../../../../../../../../Drivers/BSP/STM32WLxx_Nucleo -I../../../../../../../../Utilities/trace/adv_trace -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc -I../../../../../../../../Drivers/STM32WLxx_HAL_Driver/Inc/Legacy -I../../../../../../../../Utilities/misc -I../../../../../../../../Utilities/sequencer -I../../../../../../../../Utilities/timer -I../../../../../../../../Utilities/lpm/tiny_lpm -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32WLxx/Include -I../../../../../../../../Middlewares/Third_Party/SubGHz_Phy -I../../../../../../../../Drivers/CMSIS/Include -I"C:/Repositories/ECE_406/Projects/NUCLEO-WL55JC/Applications/SubGHz_Phy/SubGHz_Phy_PingPong_DualCore/STM32CubeIDE/CM4/Application/User/Includes" -Og -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Application-2f-User-2f-Common-2f-System

clean-Application-2f-User-2f-Common-2f-System:
	-$(RM) ./Application/User/Common/System/sys_debug.cyclo ./Application/User/Common/System/sys_debug.d ./Application/User/Common/System/sys_debug.o ./Application/User/Common/System/sys_debug.su

.PHONY: clean-Application-2f-User-2f-Common-2f-System

