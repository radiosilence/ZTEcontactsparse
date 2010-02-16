<?php

/**
 * Takes in an Outlook CSV and spits out an XML file for importing into 3's weird suite thing.
 */

$elements = array();

define( "STR_DELIM", '"' );
define( "DELIM", "," );
define( "UTF8_BUG", 1 );

function parse_csv( $string )
{
	$lines = explode_lines( $string );
	
	$headers = parse_line( array_shift( $lines ) );
	
	foreach( $lines as $line )
	{
		$outs[] = parse_line( $line, $headers );
	}
	
	return $outs;
}

function explode_lines( $string )
{
	$n = 0;
	$instring = 0;
	for( $i = 0; $i < strlen( $string ); $i++ )
	{
		$c = $string[ $i ];
		if( !$instring && $c == "\"" )
		{
			$instring = 1;
		}
		else if( $c == "\"" )
		{
			$instring = 0;
		}
		if( !$instring && $c == "\n" )
		{
			$n++;
		}
		else
		{
			$outs[ $n ] .= $c;
		}
	}
	return $outs;
}

function parse_line( $line, $headers = 0 )
{
	$n = 0;
	$hds = is_array( $headers ) ? 1 : 0;
	$instring = 0;
	
	for( $i = 0; $i < strlen( $line ); $i++ )
	{
		if( UTF8_BUG )
		{
			$c = utf8_encode( $line[ $i ] );
		}
		else
		{
			$c = $line[ $i ];
		}
		
		if( !$escaping )
		{
			if( $c == "\\" )
			{
				$escaping = 1;
			}
			else if( $instring && $c == STR_DELIM )
			{	
				$instring = 0;
			}
			else if( $instring && $c != STR_DELIM )
			{
				$out[ $hds ? $headers[ $n ] : $n ] .= $c;
			}
			else if( !$instring && $c == DELIM )
			{
				$n++;
			}
			else if( !$instring && $c == STR_DELIM )
			{
				$instring = 1;
			}
			else
			{
				$out[ $hds ? $headers[ $n ] : $n ] .= $c;
			}
		}
		if( $escaping )
		{
			$out[ $hds ? $headers[ $n ] : $n ] .= $c;
			$escaping = 0;
		}
	}
	
	return $out;
}

function map_fields( $entries, $map, $necessary )
{
	foreach( $entries as $en => $entry )
	{
		foreach( $necessary as $k => $v )
		{
			if( is_numeric( $k ) )
			{
				$k = $v;
				$v = null;
			}
			$outs[ $en ][ $k ] = $v;
		}
		
		foreach( $map as $field => $item )
		{
			if( !is_array( $item ) )
			{
				$item = array( $item );
			}
			
			foreach( $item as $iname )
			{
				if( strlen( $entry[ $iname ] ) > 0 )
				{
					$outs[ $en ][ $field ][] = trim( $entry[ $iname ] );
				}
			}
			if( count( $outs[ $en ][ $field ] ) > 0 )
			{
				$outs[ $en ][ $field ] = implode( " ", $outs[ $en ][ $field ] );
			}
		}
	}
	
	return $outs;
}

function generate_xml( $arr )
{
	foreach( $arr as $k => $v )
	{
		$xmls[ $k ] .= "<ChildInfo DataType=\"PB\">";
		foreach( $v as $field => $value )
		{
			if( strlen( $value ) > 0 )
			{
				$xmls[ $k ] .= sprintf( "\n\t" . '<%2$s>%1$s</%2$s>', $value, $field );		
			}
			else
			{
				$xmls[ $k ] .= sprintf( "\n\t" . '<%s/>', $field );
			}
		}
		$xmls[ $k ] .= "\n</ChildInfo>";
	}
	return implode( "\n", $xmls );
}

$csv = parse_csv( file_get_contents( "contacts.csv" ) );

$map = array(
	"szName" => array( "First Name", "Middle Name", "Last Name" ),
	"szEmail" => "E-mail Address",
	"szPhoneNumber0" => "Mobile Phone",
	"szPhoneNumber1" => "Home Phone",
	"szPhoneNumber4" => "Business Phone",
	"szCompany" => "Company",
);


$necessary = array( 
	"eLocation" => 1,
	"uGroupId" => 3,
	"uSize" => 0,
	"szName",
	"szCompany",
	"szDuty",
	"szEmail",
	"szOtherEmail",
	"szHomeEmail",
	"szNotes",
	"uAvailableNumber" => 0,
	"szPhoneName0",
	"szPhoneNumber0",
	"szPhoneName1",
	"szPhoneNumber1",
	"szPhoneName2",
	"szPhoneNumber2",
	"szPhoneName3",
	"szPhoneNumber3",
	"szPhoneName4",
	"szPhoneNumber4",
	"szUrl",
);

$mapped = map_fields( $csv, $map, $necessary );


$elements = generate_xml( $mapped );

$backup = "<?xml version=\"1.0\"?><root><Info><Location>1</Location><Version>3</Version><PB>true</PB><SMS>false</SMS></Info>\n" . $elements . "</root>";

echo $backup;
?>