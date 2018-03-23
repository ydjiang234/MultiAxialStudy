source D:/Git/OPS/Shared_Proc/Analysis.tcl

#Input data

set D 219.0;
set t 4.7;
set L 1350.0;
set N_axial 0.0;
set fc 29.6558779968;
set Ec [expr 4700.0 * pow($fc, 0.5)];
set ec [expr $fc / $Ec * 2.0];
set bc 0.04;
set dc 0.01;
set rc [expr 1. - $dc];
set fyt 433.244899963;
set fyn 433.244899963;
set Es 200000.0;
set bt 0.008;
set bn 0.008;
set tol 0.001;
set iter_max 100;
set d_incr 0.1;
set DispList [list 0.0 135.0];
set outname C219-5-Ru15.out;
set D_div 36;
set R_div 10;
set t_div 2;
set section_no 15;
set top_node [expr $section_no+1];
#set pi 3.1415926;
#set Ac [expr $pi * pow($D - 2.*$t,2) / 4.0];
#set As [expr $pi * pow($D,2) / 4.0 - $Ac];

wipe;
model basic -ndm 2 -ndf 3;

#Node
set i 1;
while {$i <= [expr $section_no + 1]} {
	node $i 0.0 [expr $L / $section_no * ($i - 1.0)] 0.0;
	set i [expr $i + 1];
}
fix 1 1 1 1;

#Create material;
set Mat_Con 1;
set Mat_Steel 2;
#uniaxialMaterial Concrete02 $matTag $fpc $epsc0 $fpcu $epsU $lambda $ft $Ets
uniaxialMaterial Concrete02 $Mat_Con -$fc -$ec [expr -$rc * $fc] [expr -$ec - $dc * $fc / $bc / $Ec] 0.4 [expr 0.1 * $fc] [expr 0.1 * $Ec];
#uniaxialMaterial SteelMPF $mattag $fyp $fyn $E0 $bp $bn $R0 $a1 $a2 <$a3 $a4>
#uniaxialMaterial Steel01 $Mat_Steel $fyt $Es $bt
uniaxialMaterial SteelMPF $Mat_Steel $fyt $fyn $Es $bt $bn 20.0 0.925 0.15;

#uniaxialMaterial Steel02 $Mat_Steel $fyt $Es $bt 20.0 0.925 0.15

#Create Section; 
set Sec 1
section Fiber $Sec {
	patch circ $Mat_Con $D_div $R_div 0.0 0.0 0.0 [expr $D/2-$t] 0.0 360.0;
	patch circ $Mat_Steel $D_div $t_div 0.0 0.0 [expr $D/2-$t] [expr $D/2] 0.0 360.0;
};

geomTransf Corotational 1;
#element dispBeamColumn $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag <-mass $massDens> <-cMass> <-integration $intType>
set i 1;
while {$i <= $section_no} {
	element dispBeamColumn $i $i [expr $i + 1] 10 $Sec 1;
	set i [expr $i + 1];
}

#Axial
if {$N_axial != 0.0} {
	pattern Plain 2 "Linear" {
		load $top_node 0.0 [expr -$N_axial * 1000.0] 0.0 ;
	};

	integrator LoadControl 0.1;
	system ProfileSPD;
	test RelativeEnergyIncr 1e-4 150;
	numberer Plain;
	constraints Plain;
	algorithm Newton;
	analysis Static;
	analyze 10;
	loadConst -time 0.0;
	puts "Axial Loaded"
}

pattern Plain 1 "Linear" {
	load $top_node 1000.0 0.0 0.0;
};

recorder Node -file "${outname}_moment.out" -node 1 -dof 3 reaction;
recorder Node -file "${outname}_disp.out" -node $top_node -dof 1 disp;

set AlgOrder [list Newton NewtonLineSearch]
constraints Plain;
numberer Plain;
system BandGeneral;
set isFinish [Analyse_Static_Disp_Cyclic_Control $top_node 1 $DispList $d_incr $tol $iter_max $AlgOrder]
