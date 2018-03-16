proc Analyse_Static_Disp_Control_Incr {control_node control_dof d_incr d_tol iter_max {reduce_num 3}} {
    set cur_incr $d_incr;
    set cur_reduce_num 0;
    set if_increase_tol 0;
    set if_change_alg 0;
    set is_break 0;
    integrator DisplacementControl $control_node $control_dof $cur_incr;
    test NormDispIncr $d_tol $iter_max 0;
    algorithm Newton;
    analysis Static;
    set ok [analyze 1];
    while {$ok < 0} {
        if {$cur_reduce_num < $reduce_num} {
            set cur_incr [expr $cur_incr / 10.0];
            set cur_reduce_num [expr $cur_reduce_num + 1];
            integrator DisplacementControl $control_node $control_dof $cur_incr;
            #algorithm NewtonLineSearch;
            analysis Static;
            puts $cur_reduce_num
            set ok [analyze 1]; 
            
        } elseif { $if_increase_tol==0} {
            test NormDispIncr $d_tol [expr $iter_max * 2] 0;
            set if_increase_tol 1;
            set ok [analyze 1]; 
        } elseif {$if_change_alg==0} {
            algorithm BFGS;
            set ok [analyze 1]; 
            set if_change_alg 1;
        } else {
            set is_break 1;
            break;
        }
    }
    if {$is_break==1} {
        return -1;
    } else {
        return [expr abs($cur_incr)];
    }
}

proc Analyse_Static_Disp_Control {control_node control_dof d_max d_incr d_tol iter_max fileID L top_node {reduce_num 4}} {
    if {$d_max>= 0.0} {set d_incr [expr abs($d_incr)]} else {set d_incr [expr -abs($d_incr)]}
    set is_finish 0;
    set d_cum 0.0;
    while {$d_cum < [expr abs($d_max)]} {
        #puts $d_cum
        set cur_incr [Analyse_Static_Disp_Control_Incr $control_node $control_dof $d_incr $d_tol $iter_max $reduce_num] 
        if {$cur_incr != -1} {
            #set temp [eleResponse 1 forces];
            #set Mom [lindex $temp 2];
            #set Load [expr $Mom / $L / 1000.0];
            #set cur_Disp [nodeDisp $top_node 1];
            #set data "$cur_Disp $Load";
            #puts $fileID $data;
            set d_cum [expr $d_cum + $cur_incr];
        } else {
            set is_finish -1;
            break
        }
    }
    return $is_finish;
}


proc Analyse_Static_Disp_Cyclic_Control {control_node control_dof drift_ratios d_incr d_tol iter_max fileID L top_node {reduce_num 4}} {
    set step_num [llength $drift_ratios];
    for {set i 0} {$i<$step_num-1} {incr i} {
        set d1 [lindex $drift_ratios $i];
        set d2 [lindex $drift_ratios [expr $i+1]];
        set d_max_cur [expr ($d2-$d1) * $L];
        set is_finish [Analyse_Static_Disp_Control $control_node $control_dof $d_max_cur $d_incr $d_tol $iter_max $fileID $L $top_node $reduce_num];
        if {$is_finish == -1} {
            break
        }
    }
    return $is_finish;
}
