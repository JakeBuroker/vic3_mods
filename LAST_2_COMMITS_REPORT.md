# Последние 2 коммита — диффы по строкам

Ниже — запись изменений в формате diff/hunk по каждому измененному файлу (без аналитики).

## Коммит `2fbd4222bd2aaaf3bfe1a478503b890f68b672bf` (`PSC latest`)

### `PSC/.metadata/metadata.json`
```diff
@@ -1,7 +1,7 @@
 {
   "name" : "[1.12] Private Sector Construction",
   "id" : "3420714166",
-  "version" : "1.3.5",
+  "version" : "1.3.6",
   "supported_game_version" : "",
   "short_description" : "Allows private sector and market driven construction",
   "tags" : [
```

### `PSC/common/script_values/PSC_construction_values.txt`
```diff
@@ -689,7 +689,15 @@ state_construction_allocation = {
 		limit = {
 			scope:estimated_price > local_var:state_construction_base_price
 		}
+
 		value = var:state_construction_production
+		if = {
+			# deal with case where integer limit is being reached
+			limit = {
+				var:state_construction_production > integer_max_safety_limit
+			}
+			divide = sqrt_scale_sq
+		}
 		multiply = {
 			value = 4
 			multiply = local_var:state_construction_spending
@@ -717,6 +725,13 @@ state_construction_allocation = {
 		}
 		save_temporary_value_as = num_to_sqrt
 		value = calculate_sqrt
+		if = {
+			# deal with case where integer limit is being reached
+			limit = {
+				var:state_construction_production > integer_max_safety_limit
+			}
+			multiply = sqrt_scale
+		}
 		multiply = define:NEconomy|PRICE_RANGE
 		add = {
 			value = var:state_construction_production
```

### `PSC/common/script_values/PSC_set_values.txt`
```diff
@@ -48,4 +48,7 @@ error_accuracy_denominator = {
 
 weekly_income_multiplier_base = {
     value = 2
-}
\ No newline at end of file
+}
+integer_max_safety_limit = 100000
+sqrt_scale = 100
+sqrt_scale_sq = 10000
\ No newline at end of file
```

### `PSC/common/scripted_effects/PSC_scripted_effects.txt`
```diff
@@ -235,6 +235,7 @@ set_construction_point_demand = {
                             min = 1
                         }
                         subtract = 1
+                        subtract = modifier:building_throughput_add
                     }
                 }
                 add_modifier = {
```

---

## Коммит `2ffaa7227cedc5ab7c5db0dee0c2ba1b565625fd` (`E&F latest`)

### `E&F/common/decisions/00_ef_nw_decisions.txt` (new file)
```diff
@@ -0,0 +1,109 @@
+﻿law_encouranging_childbirth_Decision_0 = {
+	is_shown = { 
+		is_ai = no
+	}
+
+	possible = {
+	}
+
+	ai_chance = {
+		base = 0
+    }
+
+	when_taken = {
+		remove_modifier = need_workforce_modifier 
+	}
+} 
+law_encouranging_childbirth_Decision_1 = {
+	is_shown = { 
+		is_ai = no
+	}
+
+	possible = {
+	}
+
+	ai_chance = {
+		base = 0
+    }
+
+	when_taken = {
+		remove_modifier = need_workforce_modifier
+		add_modifier = {
+			name = need_workforce_modifier
+			multiplier = 1
+		} 
+	}
+} 
+law_encouranging_childbirth_Decision_5 = {
+	is_shown = { 
+		is_ai = no
+	}
+
+	possible = {
+	}
+
+	ai_chance = {
+		base = 0
+    }
+
+	when_taken = {
+		remove_modifier = need_workforce_modifier
+		add_modifier = {
+			name = need_workforce_modifier
+			multiplier = 5
+		} 
+	}
+} 
+law_encouranging_childbirth_Decision_10 = {
+	is_shown = { 
+		is_ai = no
+	}
+
+	possible = {
+	}
+
+	ai_chance = {
+		base = 0
+    }
+
+	when_taken = {
+		remove_modifier = need_workforce_modifier
+		add_modifier = {
+			name = need_workforce_modifier
+			multiplier = 10
+		} 
+	}
+} 
+law_encouranging_childbirth_Decision_X = {
+	is_shown = { 
+		is_ai = no
+	}
+
+	possible = {
+	}
+
+	ai_chance = {
+		base = 0
+    }
+
+	when_taken = {
+		hidden_effect = {
+			every_scope_pop = {
+				set_pop_literacy = {
+					literacy_rate = {
+						value = root.literacy_rate
+						add = 0.25
+					}
+				}
+			}
+		}
+		custom_tooltip = IncreasePopLiteracy_Decision_cp
+	} 
+} 
```

### `E&F/common/history/states/01_ef_states.txt`
```diff
@@ -62,7 +62,7 @@
     s:STATE_SICHUAN = {
         every_scope_state = { add_modifier = { name = silver_mine_max_level multiplier = 13 } }
     }
-    s:STATE_ANDALUSIA = {
+    s:STATE_LOWER_ANDALUSIA = {
         every_scope_state = { add_modifier = { name = silver_mine_max_level multiplier = 10 } }
     }
     s:STATE_ESTREMADURA = {
```

### `E&F/common/script_values/00_financial_scripted_value.txt`
Короткая аналитика: визуально огромный diff, но это в основном whitespace/форматирование по всему файлу.  
По факту логики (при сравнении без учета пробелов) удалены только пустые строки в конце.
```diff
# В этом файле огромный форматный diff (пробелы/выравнивание).
# Значимый (ignore-whitespace) diff:
@@ -61707,6 +61707,3 @@ leading_producer_of_oil = {
 		add = 1
 	}
 }
-
-
-
```

### `E&F/common/scripted_effects/01_economic_scripted_effects.txt`
```diff
@@ -10660,7 +10660,7 @@ global_monetary_reference_reset = {
 						or = {
 							is_subject_custom_trigger = yes
 							market_owner_is_root_univ_with_buiding = yes
-						}
+						} 
 					}
 				}
 				devaluation_money_value_target = yes
@@ -10674,7 +10674,10 @@ global_monetary_reference_reset = {
 				every_country = {
 					limit = {
 						is_player = yes
-					}
+						scope:target_country = {
+							scripted_money_value_target = no #test empeche UK et Mex d'avoir une notification pour indiquer une modification de parité inverse
+						} 
+ 					}
 					trigger_event = 00_ef_economic_event.31
 				}

@@ -10691,7 +10694,7 @@ global_monetary_reference_reset = {
 						or = {
 							is_subject_custom_trigger = yes
 							market_owner_is_root_univ_with_buiding = yes
-						}
+						} 
 					}
 				}
 				revaluation_money_value_target = yes
@@ -10705,11 +10708,13 @@ global_monetary_reference_reset = {
 				every_country = {
 					limit = {
 						is_player = yes
+						scope:target_country = {
+							scripted_money_value_target = no #test empeche UK et Mex d'avoir une notification pour indiquer une modification de parité inverse
+						} 
 					}
 					trigger_event = 00_ef_economic_event.32
 				}
-
-
+ 
 				remove_modifier = revaluation_currency_target
 				add_modifier = {
 					name = revaluation_currency_target
```

### `E&F/common/scripted_guis/00_stockpile_scripted_guis.txt`
```diff
@@ -16904,37 +16904,37 @@ trade_rubber_budget_panel_show = {
 	}
 }
 
-#ammunition
-trade_ammunition_budget_panel = {
-	effect = {
-		set_variable = {
-			name = trade_grain_budget_panel
-			value = 0
-		}
-	}
-}
-
-trade_ammunition_budget_panel_show = {
-	is_shown = {
-		var:trade_ammunition_budget_panel = 1
-	}
-}
-
-#small_arms
-trade_small_arms_budget_panel = {
-	effect = {
-		set_variable = {
-			name = trade_grain_budget_panel
-			value = 0
-		}
-	}
-}
-
-trade_small_arms_budget_panel_show = {
-	is_shown = {
-		var:trade_small_arms_budget_panel = 1
-	}
-}
+# #ammunition
+# trade_ammunition_budget_panel = {
+# 	effect = {
+# 		set_variable = {
+# 			name = trade_grain_budget_panel
+# 			value = 0
+# 		}
+# 	}
+# }
+
+# trade_ammunition_budget_panel_show = {
+# 	is_shown = {
+# 		var:trade_ammunition_budget_panel = 1
+# 	}
+# }
+
+# #small_arms
+# trade_small_arms_budget_panel = {
+# 	effect = {
+# 		set_variable = {
+# 			name = trade_grain_budget_panel
+# 			value = 0
+# 		}
+# 	}
+# }
+
+# trade_small_arms_budget_panel_show = {
+# 	is_shown = {
+# 		var:trade_small_arms_budget_panel = 1
+# 	}
+# }
```

### `E&F/common/static_modifiers/00_ef_dynamic_modifier_country.txt`
```diff
@@ -22,11 +22,11 @@ need_workforce_modifier = {
 	#country_weekly_innovation_max_add = 150
 	#country_tech_spread_add = 1
 
-	country_wage_cultural_erasure_mult = 10
-	country_wage_full_acceptance_mult = 10
-	country_wage_open_prejudice_mult = 10
-	country_wage_second_rate_citizen_mult = 10
-	country_wage_violent_hostility_mult = 10
+	# country_wage_cultural_erasure_mult = 10
+	# country_wage_full_acceptance_mult = 10
+	# country_wage_open_prejudice_mult = 10
+	# country_wage_second_rate_citizen_mult = 10
+	# country_wage_violent_hostility_mult = 10
@@ -261,10 +261,10 @@ down_base_rate = {
 }
 
 devaluation_currency_target = {
-	icon = gfx/interface/icons/timed_modifier_icons/devaluation_currency.dds
+	icon = gfx/interface/icons/timed_modifier_icons/modifier_devaluation.dds
 }
 revaluation_currency_target = {
-	icon = gfx/interface/icons/timed_modifier_icons/revaluation_currency.dds
+	icon = gfx/interface/icons/timed_modifier_icons/modifier_revaluation.dds
 }
```

### `E&F/gui/00_ef_deported_gui_1.gui`
```diff
@@ -109603,7 +109603,7 @@ types market_states_panel
 												size = { 65 65 }
 
 												blockoverride "icon" {
-													texture = "gfx/interface/icons/goods_icons/manowars.dds"
+													texture = "gfx/interface/icons/goods_icons/man_o_wars.dds"
 												}
@@ -109738,7 +109738,7 @@ types market_states_panel
 												size = { 65 65 }
 
 												blockoverride "icon" {
-													texture = "gfx/interface/icons/goods_icons/manowars.dds"
+													texture = "gfx/interface/icons/goods_icons/man_o_wars.dds"
 												}
@@ -109872,7 +109872,7 @@ types market_states_panel
 												size = { 65 65 }
 
 												blockoverride "icon" {
-													texture = "gfx/interface/icons/goods_icons/manowars.dds"
+													texture = "gfx/interface/icons/goods_icons/man_o_wars.dds"
 												}
@@ -110210,7 +110210,7 @@ types market_states_panel
 												size = { 65 65 }
 
 												blockoverride "icon" {
-													texture = "gfx/interface/icons/goods_icons/manowars.dds"
+													texture = "gfx/interface/icons/goods_icons/man_o_wars.dds"
 												}
@@ -110346,7 +110346,7 @@ types market_states_panel
 												size = { 65 65 }
 
 												blockoverride "icon" {
-													texture = "gfx/interface/icons/goods_icons/manowars.dds"
+													texture = "gfx/interface/icons/goods_icons/man_o_wars.dds"
 												}
@@ -110481,7 +110481,7 @@ types market_states_panel
 												size = { 65 65 }
 
 												blockoverride "icon" {
-													texture = "gfx/interface/icons/goods_icons/manowars.dds"
+													texture = "gfx/interface/icons/goods_icons/man_o_wars.dds"
 												}
@@ -133650,7 +133650,7 @@ types market_states_panel
 
 				#transfert_currency_to_investement_pool ok
 				flowcontainer  = {
-					#visible = "[GetScriptedGui('transfert_currency_to_investement_pool').IsShown( GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
+					visible = "[GetScriptedGui('transfert_currency_to_investement_pool').IsShown( GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
 					parentanchor = hcenter
 					direction = vertical
```

### `E&F/gui/ef_dev_and_custom_windows/ef_custom_windows.gui`
```diff
@@ -46222,6 +46222,35 @@ default_popup = {
 							autoresize = yes
 						}
 
+
+						textbox = {
+							text = "building_trade_center_lvl [GetPlayer.MakeScope.ScriptValue('building_trade_center_lvl')|D]"
+							#text = "YYYY [GetPlayer.MakeScope.Var('YYYYYYYY').GetValue|D]"
+							#text = "stockpiling_dye_var_global [GetGlobalVariable('stockpiling_dye_var_global').GetValue|D]"
+
+							align = left|nobaseline
+							elide = right
+							default_format = "#white #bold"
+							autoresize = yes
+						}
+
+
+						textbox = {
+							text = "building_financial_district_lvl [GetPlayer.MakeScope.ScriptValue('building_financial_district_lvl')|D]"
+							#text = "YYYY [GetPlayer.MakeScope.Var('YYYYYYYY').GetValue|D]"
+							#text = "stockpiling_dye_var_global [GetGlobalVariable('stockpiling_dye_var_global').GetValue|D]"
+
+							align = left|nobaseline
+							elide = right
+							default_format = "#white #bold"
+							autoresize = yes
+						}
```

### `E&F/localization/english/00_ef_gui_localization_l_english.yml`
Короткая аналитика: это крупная чистка локализационного блока (удаление большого набора строк) + мелкая правка форматирования заголовка.  
Diff ниже дан в сокращенном виде, чтобы не раздувать документ на сотни строк.
```diff
@@ -1,4 +1,4 @@
-﻿l_english:
+﻿  l_english:
@@ -5250,84 +5250,12 @@ thaler_saxon_thaler_03_money_value:0 "#v [GetPlayer.MakeScope.ScriptValue('money
-  # ██████╗ ██╗   ██╗██╗██╗     ██████╗ ██╗███╗   ██╗ ██████╗
-  # ██╔══██╗██║   ██║██║██║     ██╔══██╗██║████╗  ██║██╔════╝
-  # ██████╔╝██║   ██║██║██║     ██║  ██║██║██╔██╗ ██║██║  ███╗
-  # ██╔══██╗██║   ██║██║██║     ██║  ██║██║██║╚██╗██║██║   ██║
-  # ██████╔╝╚██████╔╝██║███████╗██████╔╝██║██║ ╚████║╚██████╔╝
-  # ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝
+  # des
@@ -... удален блок 72 строк ...
-  ## Central Bank
-  building_bank:0 "Центральный банк"
-
-  ## Financial place
-  building_financial_centre_scripted:0 "[ROOT.GetCountry.GetCapital.GetNameNoFormatting] биржа"
-  building_financial_centre:0 "Финансовый центр"
-  ...
-  building_silver_mine:0 "Серебряные рудники"
```

### `E&F/localization/russian/00_ef_gui_localization_l_russian.yml`
```diff
@@ -1,4 +1,4 @@
-﻿l_russian:
+﻿  l_russian:
```
