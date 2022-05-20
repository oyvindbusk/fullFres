import pandas as pd
import sqlite3
import sqlalchemy
import datetime
from sqlalchemy import create_engine
from sqlalchemy import text

#sqlite syntax...
def generate_db(db):

	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		result_sample = conn.execute(text("CREATE TABLE IF NOT EXISTS sample ( \
		runid TEXT, \
		sampleid TEXT, \
		CHROM_POS_ALTEND_DATE TEXT, \
		User_Classification TEXT, \
		Variant_ID TEXT, \
		Variant_Name TEXT, \
		Key_Variant TEXT, \
		Oncomine_Reporter_Evidence TEXT, \
		Type TEXT, \
		Oncomine_Gene_Class TEXT, \
		Oncomine_Variant_Class TEXT, \
		Call TEXT, \
		Call_Details TEXT, \
		Phred_QUAL_Score TEXT, \
		Zygosity TEXT, \
		P_Value TEXT, \
		PPA TEXT, \
		Read_Counts_Per_Million TEXT, \
		Oncomine_Driver_Gene TEXT, \
		Gene_Isoform TEXT, \
		NormalizedReadCount TEXT, \
		Imbalance_Score TEXT, \
		Copy_Number TEXT, \
		P_Value_1 TEXT, \
		CNV_Confidence TEXT, \
		Valid_CNV_Amplicons TEXT, \
		ID TEXT, \
		QUAL TEXT, \
		FILTER TEXT, \
		GT TEXT, \
		GQ TEXT, \
		CN TEXT, \
		READ_COUNT TEXT, \
		GENE_NAME TEXT, \
		EXON_NUM TEXT, \
		RPM TEXT, \
		NORM_COUNT TEXT, \
		NORM_COUNT_TO_HK TEXT, \
		FUSION_DRIVER_GENE TEXT, \
		ANNOTATION TEXT, \
		PASS_REASON TEXT, \
		Non-Targeted TEXT, \
		FR TEXT, \
		PRECISE TEXT, \
		END TEXT, \
		NUMTILES TEXT, \
		SD TEXT, \
		CDF_MAPD TEXT, \
		RAW_CN TEXT, \
		REF_CN TEXT, \
		PVAL TEXT, \
		CI TEXT, \
		AF TEXT, \
		AO TEXT, \
		DP TEXT, \
		FAO TEXT, \
		FDP TEXT, \
		FDVR TEXT, \
		FR TEXT, \
		FRO TEXT, \
		FSAF TEXT, \
		FSAR TEXT, \
		FSRF TEXT, \
		FSRR TEXT, \
		FWDB TEXT, \
		FXX TEXT, \
		GCM TEXT, \
		HRUN TEXT, \
		HS_ONLY TEXT, \
		LEN TEXT, \
		MLLD TEXT, \
		OALT TEXT, \
		OID TEXT, \
		OMAPALT TEXT, \
		OPOS TEXT, \
		OREF TEXT, \
		PB TEXT, \
		PBP TEXT, \
		PPD TEXT, \
		QD TEXT, \
		RBI TEXT, \
		REFB TEXT, \
		REVB TEXT, \
		RO TEXT, \
		SAF TEXT, \
		SAR TEXT, \
		SPD TEXT, \
		SRF TEXT, \
		SRR TEXT, \
		SSEN TEXT, \
		SSEP TEXT, \
		SSSB TEXT, \
		STB TEXT, \
		STBP TEXT, \
		VARB TEXT, \
		NID TEXT, \
		MISA TEXT, \
		CLSF TEXT, \
		VCFALT TEXT, \
		VCFPOS TEXT, \
		VCFREF TEXT, \
		HS TEXT, \
		SUBSET TEXT, \
		MISC TEXT, \
		PRIMARY KEY (runid, sampleid, CHROM_POS_ALTEND_DATE) \
        )"))
		result_variant = conn.execute(text("CREATE TABLE IF NOT EXISTS variant ( \
		CHROM_POS_ALTEND_DATE TEXT, \
		CHROM TEXT, \
		POS TEXT, \
		ID TEXT, \
		REF TEXT, \
		ALT TEXT, \
		DATE TEXT, \
		Type TEXT, \
		gene TEXT, \
		exon TEXT, \
		oncomineGeneClass TEXT, \
		oncomineVariantClass TEXT, \
		origPos TEXT, \
		origRef TEXT, \
		normalizedRef TEXT, \
		normalizedPos TEXT, \
		normalizedAlt TEXT, \
		gt TEXT, \
		codon TEXT, \
		coding TEXT, \
		transcript TEXT, \
		function TEXT, \
		protein TEXT, \
		location TEXT, \
		origAlt TEXT, \
		CLNACC1 TEXT, \
		CLNSIG1 TEXT, \
		CLNREVSTAT1 TEXT, \
		CLNID1 TEXT, \
		polyphen TEXT, \
		sift TEXT, \
		grantham TEXT, \
		PRIMARY KEY (CHROM, POS, ALT, DATE) \
        )"))
		result_interpretation = conn.execute(text("CREATE TABLE IF NOT EXISTS interpretation ( \
		runid TEXT, \
		sampleid TEXT, \
		GENLISTE TEXT, \
		chrom_pos_ref_alt_date TEXT, \
		SVARES_UT TEXT, \
		POPULASJONSDATA TEXT, \
		FUNKSJONSSTUDIER TEXT, \
		PREDIKTIVE_DATA TEXT, \
		CANCER_HOTSPOTS TEXT, \
		COMPUTATIONAL_EVIDENCE TEXT, \
		KONSERVERING TEXT, \
		ANDRE_DB TEXT, \
		KOMMENTAR TEXT, \
		ONCOGENICITY INTEGER, \
		TIER TEXT, \
		KOMMENTAR2 TEXT, \
		DATO TEXT, \
		BRUKER TEXT, \
		KONTROLL TEXT, \
		KOLONNE6 TEXT, \
		KOLONNE7 TEXT, \
		KOLONNE8 TEXT, \
		KOLONNE9 TEXT, \
		KOLONNE10 TEXT, \
		KOLONNE11 TEXT, \
		PRIMARY KEY (RUNID, SAMPLEID, chrom_pos_ref_alt_date) \
		)"))
		stmt = "create view if not exists all_data as select * \
			from vcf \
			left join variant \
			on vcf.chrom_pos_ref_alt_date = variant.chrom_pos_ref_alt_date \
			left join interpret \
			on vcf.chrom_pos_ref_alt_date = interpret.chrom_pos_ref_alt_date \
			and vcf.runid = interpret.runid \
			and vcf.sampleid = interpret.sampleid;"
		result_all = conn.execute(text(stmt))

def populate_vcf_variantdb(db, dfvcf, dfvariant, run_id, sample_id):
	# add variants to table vcf and add variants if new to table variant
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	if dfvcf.empty:
		print("Missing data to import to tables Variant and Vcf")
		return

	dfvcf_copy = dfvcf.copy(deep=True)
	dfvariant_copy = dfvariant.copy(deep=True)
	# add chrom_pos_ref_alt_date column
	dfvcf_copy.insert(0, 'runid', run_id, True)
	dfvcf_copy.insert(1, 'sampleid', sample_id, True)
	dfvcf_copy.insert(2, 'chrom_pos_ref_alt_date', "" )
	dfvariant_copy.insert( 0, 'chrom_pos_ref_alt_date', "" )
	# add date column
	date=datetime.datetime.now().strftime("%y%m%d%H%M%S")
	dfvariant_copy.insert(6, 'DATE', date)
	dfvariant_copy["POS"]=dfvariant_copy["POS"].astype(str)
	dfvariant_copy.chrom_pos_ref_alt_date = \
		dfvariant_copy[["CHROM", "POS", "REF", "ALT", "DATE"]].agg("".join, axis=1)

	# Connecting to sqlite database
	with engine.connect() as conn:
		#BRUK kombinasjon chrom,pos,ref,alt og sjekk om denne er med i variant-tabell 
		for row in range(len(dfvcf_copy)):
			stmt = "select * from variant \
				where CHROM = '"+dfvariant_copy.CHROM[row]+"' \
					AND POS = '"+dfvariant_copy.POS[row]+"' \
					AND REF = '"+dfvariant_copy.REF[row]+"' \
					AND ALT = '"+dfvariant_copy.ALT[row]+"';"
			dfdb_variant = pd.read_sql_query(text(stmt), con = conn)

			#hvis med: sjekk hvis den er lik den som skal legges in

			if not dfdb_variant.empty:
				dfdb_variant_latest = dfdb_variant[ dfdb_variant.chrom_pos_ref_alt_date == \
					dfdb_variant.chrom_pos_ref_alt_date.max() ]
				# get columns from database
				stmt_col = "pragma table_info(variant);"
				db_col = pd.read_sql_query(text(stmt_col), con = conn)
				db_col = db_col[db_col.name != 'DATE']
				db_col = db_col[db_col.name != 'chrom_pos_ref_alt_date']

				dfvariant_copy = dfvariant_copy.astype(str)
				dfdb_variant_latest = dfdb_variant_latest.astype(str)
				# check if variant in database except key chrom_pos_ref_alt_date
				variantindb = dfdb_variant_latest.reset_index(drop=True)[db_col].equals( \
					dfvariant_copy.loc[[row]].reset_index(drop=True)[db_col])

				if variantindb:
					# if in db: use key in variant table (chrom_pos_ref_alt_date) as key to vcf table
					# do not add variant to table variant
					# if sample, run and variant already in vcf database don't add
					dfvariant_copy = dfvariant_copy.drop(row)
					dfvcf_copy.chrom_pos_ref_alt_date.loc[row] = dfdb_variant_latest.chrom_pos_ref_alt_date.iloc[0]
					print (dfvcf_copy.chrom_pos_ref_alt_date.loc[row])
					stmtvcf = "select * from vcf \
						where runid = '"+dfvcf_copy.runid.loc[row]+"' \
							AND sampleid = '"+dfvcf_copy.sampleid.loc[row]+"' \
							AND chrom_pos_ref_alt_date = '"+dfvcf_copy.chrom_pos_ref_alt_date.loc[row]+"';"
					dfdb_vcf = pd.read_sql_query(text(stmtvcf), con = conn)
					if not dfdb_vcf.empty:
						print(dfvcf_copy.runid.loc[row], \
							dfvcf_copy.sampleid.loc[row], \
								dfvcf_copy.chrom_pos_ref_alt_date.loc[row], " is already in database")
						dfvcf_copy = dfvcf_copy.drop(row)
				else:
					# if not in db, i.e existing variant but with new FUNC
					dfvcf_copy.chrom_pos_ref_alt_date.loc[row] = dfvariant_copy.chrom_pos_ref_alt_date.loc[row]

			else:
				# if variant not previously in database, add new variant
				dfvcf_copy.chrom_pos_ref_alt_date.loc[row] = dfvariant_copy.chrom_pos_ref_alt_date.loc[row]

		del dfvcf_copy["CHROM"]
		del dfvcf_copy["POS"]
		del dfvcf_copy["REF"]
		del dfvcf_copy["ALT"]
		del dfvcf_copy["FUNC"]
		dfvcf_copy.to_sql('vcf', con=conn, if_exists='append', index=False)
		if not dfvariant_copy.empty:
			dfvariant_copy["POS"]=dfvariant_copy["POS"].astype(str)
			dfvariant_copy.to_sql('variant', con=conn, if_exists='append', index=False)
		conn.commit()	

#BRUK kombinasjon chrom,pos,ref,alt og sjekk om denne er med i variant-tabell 
#	hvis med 
#		sjekk hvis den er lik den som skal legges in
#			hvis lik
#				bruk key (chrom_pos_ref_alt_date) som nokkel i vcf-tabell
#			hvis forskjellig
#				lag chrom_pos_ref_alt_date
#				legg inn ny post i variant-tabell med key (chrom_pos_ref_alt_date)
#				bruk key (chrom_pos_ref_alt_date) som nokkel i vcf-tabell

def populate_interpretdb(db, df_interpret, chrom_pos_ref_alt_date):
	# Only one entry
	df_interpret_copy = df_interpret.copy(deep=True)
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		stmt = "select * from interpret \
				where chrom_pos_ref_alt_date = '"+chrom_pos_ref_alt_date+"' \
					AND runid = '"+df_interpret_copy.runid.iloc[0]+"' \
					AND sampleid = '"+df_interpret_copy.sampleid.iloc[0]+"';"
		dfdb_interpret = pd.read_sql_query(text(stmt), con = conn)
		if dfdb_interpret.empty:
			df_interpret_copy["POS"]=df_interpret_copy["POS"].astype(str)
			df_interpret_copy.insert(3, 'chrom_pos_ref_alt_date', chrom_pos_ref_alt_date)
			del df_interpret_copy["CHROM"]
			del df_interpret_copy["POS"]
			del df_interpret_copy["REF"]
			del df_interpret_copy["ALT"]
			df_interpret_copy.to_sql('interpret', con=conn, if_exists='append', index=False)
			conn.commit()
		else:
			print("Entry already in database")
			return

#sqlite syntax - rewrite ...
def count_variant(db, chrom, pos, ref, alt, table):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    stmt = "SELECT COUNT(*) \
			FROM "+table+" \
            WHERE \
            	CHROM = '"+chrom+"' AND \
            	POS = '"+pos+"' AND \
				REF = '"+ref+"' AND \
            	ALT = '"+alt+"' \
            ;"
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        for row in result:
            return row[0]

def list_runandsample_variant(db, chrom, pos, ref, alt, table):
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	pos = str(pos)
	stmt = "select \
				runid, sampleid \
			from \
				"+table+" \
			where \
				chrom_pos_ref_alt = '"+chrom+pos+ref+alt+"' \
			;"
	with engine.connect() as conn:
		result = conn.execute(text(stmt))
		for row in result:
			return row
