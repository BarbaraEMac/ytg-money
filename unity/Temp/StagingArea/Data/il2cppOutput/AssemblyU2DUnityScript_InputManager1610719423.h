﻿#pragma once

#include "il2cpp-config.h"

#ifndef _MSC_VER
# include <alloca.h>
#else
# include <malloc.h>
#endif

#include <stdint.h>

#include "UnityEngine_UnityEngine_MonoBehaviour1158329972.h"

// UnityEngine.GameObject
struct GameObject_t1756533147;




#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif

// InputManager
struct  InputManager_t1610719423  : public MonoBehaviour_t1158329972
{
public:
	// UnityEngine.GameObject InputManager::pumpkinObject
	GameObject_t1756533147 * ___pumpkinObject_2;

public:
	inline static int32_t get_offset_of_pumpkinObject_2() { return static_cast<int32_t>(offsetof(InputManager_t1610719423, ___pumpkinObject_2)); }
	inline GameObject_t1756533147 * get_pumpkinObject_2() const { return ___pumpkinObject_2; }
	inline GameObject_t1756533147 ** get_address_of_pumpkinObject_2() { return &___pumpkinObject_2; }
	inline void set_pumpkinObject_2(GameObject_t1756533147 * value)
	{
		___pumpkinObject_2 = value;
		Il2CppCodeGenWriteBarrier(&___pumpkinObject_2, value);
	}
};

#ifdef __clang__
#pragma clang diagnostic pop
#endif
