#pragma once

#include "il2cpp-config.h"

#ifndef _MSC_VER
# include <alloca.h>
#else
# include <malloc.h>
#endif

#include <stdint.h>

#include "UnityEngine_UnityEngine_MonoBehaviour1158329972.h"
#include "UnityEngine_UnityEngine_Color2020392075.h"





#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif

// PumpkinManager
struct  PumpkinManager_t87430429  : public MonoBehaviour_t1158329972
{
public:
	// UnityEngine.Color PumpkinManager::pumpkinOrange
	Color_t2020392075  ___pumpkinOrange_2;
	// System.Single PumpkinManager::topLayerDepth
	float ___topLayerDepth_3;

public:
	inline static int32_t get_offset_of_pumpkinOrange_2() { return static_cast<int32_t>(offsetof(PumpkinManager_t87430429, ___pumpkinOrange_2)); }
	inline Color_t2020392075  get_pumpkinOrange_2() const { return ___pumpkinOrange_2; }
	inline Color_t2020392075 * get_address_of_pumpkinOrange_2() { return &___pumpkinOrange_2; }
	inline void set_pumpkinOrange_2(Color_t2020392075  value)
	{
		___pumpkinOrange_2 = value;
	}

	inline static int32_t get_offset_of_topLayerDepth_3() { return static_cast<int32_t>(offsetof(PumpkinManager_t87430429, ___topLayerDepth_3)); }
	inline float get_topLayerDepth_3() const { return ___topLayerDepth_3; }
	inline float* get_address_of_topLayerDepth_3() { return &___topLayerDepth_3; }
	inline void set_topLayerDepth_3(float value)
	{
		___topLayerDepth_3 = value;
	}
};

#ifdef __clang__
#pragma clang diagnostic pop
#endif
