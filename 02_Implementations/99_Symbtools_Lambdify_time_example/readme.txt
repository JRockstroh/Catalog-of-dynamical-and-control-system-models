Lorenz_attractor_class_compare: 
	Enthält zwei "get_rhs_func" Methoden. 
	get_rhs_func_lamb: Generiert rhs-Funktion mittels sympy.lambdify 
	get_rhs_func_ST: Generiert rhs-Funktion mittels symbtools.expr_to_func 

Lorenz_test_Vergleich: 
	Vergleicht erstellte rhs-Funktionen bezüglich der Laufzeit. 
	Einmal bei Simulation mittels solve_ivp und einmal bei 100000 facher Ausführung der Funktion mit x0 = [0.1, 0.1, 0.1].
	Die Laufzeiten werden in der Konsole ausgegeben und verglichen.