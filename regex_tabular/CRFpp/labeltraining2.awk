BEGIN {FS="\t"; OFS="\t"}

# add 5th header
NR==1 { $5 = "TrainingLabel"; print; next }

# compute line variable
{
	#RC = "("   $1   ","   $2   ")"
}

# do not add training labels from lineno==145 on.
#$1 >= 145 { $5 = ""; print; next }
#$1 >= 145 { next }
$1 >= 156 { next }

# labelling:
$1==1		&&	$2==6 { $5 = "PRODUCT_CODE" ; print ; next}
$1==37	&&	$2==6 { $5 = "PRODUCT_CODE" ; print ; next}
$1==73	&&	$2==5 { $5 = "PRODUCT_CODE" ; print ; next}
$1==109	&&	$2==6 { $5 = "PRODUCT_CODE" ; print ; next}
$1==145	&&	$2==8 { $5 = "PRODUCT_CODE" ; print ; next}

$1==1		&&	$2==0 { $5 = "PRODUCT_NAME" ; print ; next}
$1==37	&&	$2==0 { $5 = "PRODUCT_NAME" ; print ; next}
$1==73	&&	$2==0 { $5 = "PRODUCT_NAME" ; print ; next}
$1==109	&&	$2==0 { $5 = "PRODUCT_NAME" ; print ; next}
$1==145	&&	$2==0 { $5 = "PRODUCT_NAME" ; print ; next}


#index("(2,0)(38,0)(74,0)(110,0)", RC)	{ $5 = "/PRODUCT_NAME" ; print ; next}
#index("(2,6)(38,6)(74,6)(110,6)", RC)	{ $5 = "/PRODUCT_CODE" ; print ; next}

$4=="Reportable" { $5 = "/Reportable" ; print ; Reportable++; next}
$4=="Managed" { $5 = "/Managed" ; print ; Managed++; next}

#Long Short Managed Money = the key table-column anchors
#index("(8,13)(44,13)(80,13)(116,13)", RC)	{ $5 = "/LONG_HEADER" ; print ; next}
#index("(8,15)(44,15)(80,15)(116,15)", RC)	{ $5 = "/SHORT_HEADER" ; print ; next}

$1==7		&&	$2==12 { $5 = "LONG_HEADER" ; print ; next}
$1==43	&&	$2==12 { $5 = "LONG_HEADER" ; print ; next}
$1==79	&&	$2==12 { $5 = "LONG_HEADER" ; print ; next}
$1==115	&&	$2==7 { $5 = "LONG_HEADER" ; print ; next}
$1==151	&&	$2==7 { $5 = "LONG_HEADER" ; print ; next}

$1==7		&&	$2==14 { $5 = "SHORT_HEADER" ; print ; next}
$1==43	&&	$2==14 { $5 = "SHORT_HEADER" ; print ; next}
$1==79	&&	$2==14 { $5 = "SHORT_HEADER" ; print ; next}
$1==115	&&	$2==9 { $5 = "SHORT_HEADER" ; print ; next}
$1==151	&&	$2==9 { $5 = "SHORT_HEADER" ; print ; next}

#All = the key table-row anchor
#index("(12,0)(48,0)(84,0)(120,0)", RC)	{ $5 = "/All_ROW" ; print ; next}

$1==11	&&	$2==0 { $5 = "All_ROW" ; print ; next}
$1==47	&&	$2==0 { $5 = "All_ROW" ; print ; next}
$1==83	&&	$2==0 { $5 = "All_ROW" ; print ; next}
$1==119	&&	$2==0 { $5 = "All_ROW" ; print ; next}
$1==155	&&	$2==0 { $5 = "All_ROW" ; print ; next}


#Cells
#index("(12,21)(48,21)(84,17)(120,23)", RC)	{ $5 = "/MMLONGVAL1000"	; print ; next}
#index("(12,23)(48,23)(84,19)(120,25)", RC)	{ $5 = "/MMLONGVAL1" 		; print ; next}
#index("(12,24)(48,24)(84,20)(120,26)", RC)	{ $5 = "/MMSHORTVAL1000"	; print ; next}
#index("(12,26)(48,26)(84,22)(120,28)", RC)	{ $5 = "/MMSHORTVAL1"		; print ; next}

$1==11	&&	$2==8 { $5 = "MMLONGVAL" ; print ; next}
$1==47	&&	$2==8 { $5 = "MMLONGVAL" ; print ; next}
$1==83	&&	$2==8 { $5 = "MMLONGVAL" ; print ; next}
$1==119	&&	$2==8 { $5 = "MMLONGVAL" ; print ; next}
$1==155	&&	$2==8 { $5 = "MMLONGVAL" ; print ; next}

$1==11	&&	$2==9 { $5 = "MMSHORTVAL" ; print ; next}
$1==47	&&	$2==9 { $5 = "MMSHORTVAL" ; print ; next}
$1==83	&&	$2==9 { $5 = "MMSHORTVAL" ; print ; next}
$1==119	&&	$2==9 { $5 = "MMSHORTVAL" ; print ; next}
$1==155	&&	$2==9 { $5 = "MMSHORTVAL" ; print ; next}


# defaults:
{ $5 = $3  ; print ; next }
