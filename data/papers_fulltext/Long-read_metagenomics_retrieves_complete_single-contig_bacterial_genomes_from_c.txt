Metagenomics is a powerful and rapidly developing approach that can be used to unravel uncultured microbial diversity and expand the tree of life, and give new biological insights into the microbes inhabiting underexplored environments [

Previous studies have reported similarities between canine and human GI microbiome. In general, different GI diseases relate to an altered GI microbiome that, on the other hand, can be modulated by diet and dietary complements (such as pre- and probiotics) (See [

Microbiome studies are predominantly either marker-specific (e.g., 16S rRNA gene for Bacteria) or whole metagenome sequencing [

The application of long-read sequencing to metagenomics enables retrieving metagenome-assembled genomes (MAGs) with high completeness. The most recent strategy in long-read metagenomics uses the long reads to obtain the draft metagenome assembly –ensuring the greatest contiguity of MAGs– and short reads to polish and improve the overall accuracy. This strategy was applied to assess the human GI microbiome [

In our previous work, we used long-read metagenomics to assess the taxonomy and reach species identification on the canine fecal microbiome. Even though we used a low-depth sequencing approach, we assembled a circular contig corresponding to an

In the present study, we use nanopore long-read metagenomics and frameshift aware correction to overcome the need for polishing with short reads. As a result, we retrieve and characterize eight high-quality MAGs and gain new biological insights into the dog fecal microbiome.

Our study focuses on the analysis of a single fecal sample of a healthy pet dog. The fecal sample used for the DNA extraction was collected when walking a healthy pet dog. We have neither altered nor manipulated the animal in any way. The dog was an adult male Beagle of 6 years and 8 months old with no recent antibiotics intake. The last time he was treated with antibiotics was three years before sampling, when he underwent a 15-day treatment with doxycycline –tetracycline-class antibiotic– due to excess secretion of mucus and saliva. A fresh sample was collected and stored at − 80 °C until further processing.

We used two different kits from Zymobiomics (Zymo Research) for DNA extraction following the manufacturer’s instructions: the Quick-DNA HMW MagBead for High-Molecular Weight DNA (without bead-beating) and the DNA Miniprep Kit, which is with a classical bead-beating based microbiome DNA extraction. Throughout the manuscript, we use HMW-DNA (high-molecular weight DNA) extraction and non-HMW DNA (no high-molecular weight DNA) extraction terms.

Each DNA extraction was sequenced in a single Flowcell R9.4.1 using MinION™ (Oxford Nanopore Technologies). The Ligation Sequencing Kit 1D (SQK-LSK109; Oxford Nanopore Technologies) was used to prepare both libraries. For non-HMW DNA, we followed the manufacturer’s protocol. For the HMW-DNA, we tuned few parameters: i) at DNA repair and end-prep step, we incubated at 20 °C for 20 min and 65 °C for 20 min; ii) we extended rotator mixer (Hula mixer) times to 10 min; iii) we extended elution time after AMPure XP beads to 10 min; iv) final incubation with elution buffer was performed at 37 °C for 15 min (as recommended for HMW-DNA).

Raw fast5 files were basecalled using Guppy 3.4.5 (Oxford Nanopore Technologies) with high accuracy basecalling mode (dna_r9.4.1_450bps_hac.cfg). During the basecalling, the reads with an accuracy lower than 7 were discarded. The detailed bioinformatics workflow can be found in Additional File

To obtain the first taxonomic assignment directly from the raw reads, we processed the data using Kraken2 2.0.8 [

We used Nanoplot 1.28 (https://github.com/wdecoster/NanoPlot) to obtain the run summary statistics, Porechop 0.2.4 (

Before proceeding with the metagenomics assembly, we performed an error-correction step of the raw nanopore reads using canu 2.0 [

We used the corrected reads to perform metagenome assembly with Flye 2.7 [

The next step for the HQ MAGs was to correct the frameshift errors, as described in [

To assess the quality of the MAGs, we used CheckM 1.1.1 [

GTDB-tk 1.3.0 [

We extracted the 16S rRNA genes from the HQ MAGs before the frameshift correction step using Anvi’o 6.1 [

Abricate 0.9.8 (

We compared the HQ MAGs obtained to previously reported MAGs from two recent gastrointestinal collections: i) the animal gut metagenome [

We retrieved MAGs that represented the same species as our HQ MAGs by keeping: i) those with > 95% of ANI [

We performed a pangenome analysis for each bacterial species using Anvi’o 6.2 [

We characterized the fecal microbiome of a healthy dog using long-read metagenomics with Nanopore sequencing. An overview of the complete experimental design is presented on Fig.

Experimental design overview. A single fecal sample from a healthy dog was extracted using a HMW and a non-HMW DNA extraction. Samples were sequenced using nanopore sequencing. Raw reads were basecalled and corrected prior to assembly. Four different data subsets were assembled to retrieve the maximum number of high-quality MAGs. These MAGs were frameshift-corrected and further analyzed

After high accuracy basecalling and error correction, we performed several metagenomics assembly strategies to retrieve eight single-contig high-quality MAGs (HQ MAGs), which were > 90% complete with < 5% contamination and contained most ribosomal genes and tRNAs, and three medium-quality ones (MQ MAGs). We further corrected the HQ MAGs for frameshifts errors and compared them at the functional level with those previously identified in other gastrointestinal metagenome catalogs.

HMW sequencing produced 5.81 million reads with N50 of 4369 bp and a median length of 2312 bp (total throughput: 18.76 Gbp), whereas non-HMW produced 11.13 million reads with N50 of 2102 bp and a median length of 1093 bp (total throughput: 17.29 Gbp).

We taxonomically classified all the uncorrected raw reads with Kraken2 and found 81.8% of the classified reads in HMW vs. 70.8% in non-HMW. More than 99% of the total reads corresponded to Bacteria. The most abundant phylum was Bacteroidetes (~ 80% of total reads), followed in abundance by Firmicutes (12.5% in HMW vs. 8.9% in non-HMW), Proteobacteria (~ 5%), and Fusobacteria (1.9% in HMW vs. 3.9% in non-HMW). At the genus level, this dog fecal microbiome was rich in

The metagenomics assembly with the HMW-DNA dataset was more contiguous, presenting fewer and longer contigs than the non-HMW DNA one (contigs: 1898 vs. 2944; N50: 187,680 vs. 94,109 bp) (Additional File

HMW-DNA vs. non-HMW DNA metagenomics assembly from the fecal sample of a healthy dog. Bandage plots of

In summary, HMW-DNA extraction improved the taxonomic classification of the raw unassembled reads (less unclassified reads), the metagenomics assembly contiguity, and the retrieval of longer and circular contigs (potential HQ MAGs). Thus, HMW-DNA extraction becomes the preferred choice to recover HQ MAGs directly from complex metagenomics samples.

To ensure the highest coverage and consensus accuracies for the retrieved MAGs, we further merged and assembled the HMW and the non-HMW datasets (100% dataset; 16.94 million reads, 36.05 Gbp). As we aimed to retrieve the maximum number of HQ MAGs, we performed extra metagenomics assemblies using 75 and 50% data subsets from that merged dataset (Additional File

After assigning taxonomy and comparing among assemblies, we identified non-redundant MAGs: eight HQ MAGs, and three MQ MAGs (Table

High quality (HQ) and medium quality (mq) single-contig MAGs retrieved in each metagenome assembly. Taxonomy assigned using the GTDB database release 95. Q is the MAG quality. Cov. is the coverage from Flye. *

For each HQ MAG, we selected the representative with the highest coverage –and subsequent highest consensus accuracy– for further analyses. We performed an extra step of frameshift aware correction that reduced the insertions and deletions (indels), which are the most abundant nanopore sequencing error type. The frameshift correction resulted in fewer predicted coding sequences (CDS) (Fig.

Histograms of the insertions and deletions in medium-quality MAGs (left) transformed into high-quality MAGs, after frameshift correction (right). The number of CDS, completeness (Compl.), and contamination (Cont.) are also included to evaluate the quality. Y-axis scale is 500 for better visualization of the insertions and deletions

From a single canine fecal sample, we obtained eight HQ MAGs regarding MIMAG criteria [

Summary of genome statistics for High-quality MAGs compared to representatives on the public datasets. Coverage (Cov.) and circularity (Circ.) retrieved from Flye; completeness (% Compl.), from CheckM; tRNAs and rRNA values, from PROKKA. tRNAs count refers to unique canonical tRNAs. GTDB species representative are used as the references for comparison. The two exceptions are

As we are working with nanopore-only assemblies, we can expect some uncorrected frameshift errors that lead to a larger number of pseudogenes. When compared to each representative genome, our HQ MAGs presented a higher percentage of pseudogenes in all the cases but

We assessed the prevalence of the HQ MAGs retrieved in the present study among several GI microbiome surveys, either using whole-genome data (metagenome surveys) or the 16S rRNA genes data (amplicon surveys).

On the one hand, we assessed the prevalence of our HQ MAGs in humans’ [

Prevalence of the bacterial species identified in public microbiome surveys

On the other hand, we took advantage of the fact that long-read sequencing allows retrieving complete ribosomal genes, which are universal taxonomic markers for Bacteria. So, we further extracted the 16S rRNA genes of the HQ MAGs to link them to 16S rRNA gene-based microbiome studies (Fig.

Similarity of 16S rRNA gene from Sutterella HQ MAGs to public datasets. The 16S rRNA gene comparison from

For the other five HQ MAGs without a reference genome, we identified that their 16S rRNA genes were closely related to others previously identified in wolves’ distal gut microbiome [

Finally, we performed a pangenome analysis among the HQ MAGs from our study and other genomes from the same bacterial species inhabiting different hosts to assess functional and genomic similarities (Additional File

Long reads enable to retrieve complete genes and their genomic context within a single read. Therefore, both the mobile genetic elements and the antimicrobial resistance genes assemble easily within the correct MAG.

We compared each HQ MAG’s functional potential to previously published MAGs from the same bacterial species found in GI microbiome of dogs, humans, or other animals (Fig.

Functional analysis and comparison of HQ MAGs and published bacterial species using the COG database.

Finally, we further characterized the HQ MAGs to assess their potential antimicrobial resistance. Tetracycline resistance genes were detected in

As an example of the potential of long-reads for providing genomic context, we were able to identify that

Metagenomics approaches can provide new biological insights into the microbes inhabiting underexplored environments, such as the canine fecal microbiome. Here, we applied nanopore long-read metagenomics and frameshift aware correction to a fecal sample of a healthy dog and retrieved eight HQ MAGs and three MQ MAGs.

At the technical level, we compared a HMW and non-HMW DNA extraction to perform long-read metagenomics and confirmed that a HMW-DNA extraction was the best choice. For analyses using unassembled raw reads, it improved the taxonomic classification and displayed less unclassified reads. For metagenomics assembly, it improved the contiguity and increased the retrieval of longer and circular contigs (potential HQ MAGs). This is in line with recent studies on human fecal microbiome, where they used HMW-DNA extraction together with long-read metagenomics to recover high-quality MAGs [

We tested several metagenomics assembly strategies (using HMW data only, 100, 75, and 50% of the total data) to retrieve the highest number of different HQ MAGs. The HMW data and the 75% data retrieved the highest number of HQ MAGs, but none of the performed assemblies alone retrieved the eight HQ MAGs.

The HQ MAGs belonged to

For

Despite humans and dogs share similar microbial signatures on the GI microbiome [

The genera

Finally,

Tetracycline resistance genes were found not only in the genome of

At the functional level, we detected an overrepresentation of the Mobilome COG category within most of the HQ MAGs retrieved here when compared to other MAGs –not when compared to reference genomes. Long-reads allow retrieving complete mobile genetic elements together with their genomic context facilitating its assembly to the proper MAG. This advantage was also reported in metagenomics studies that include short- and long-reads in their assemblies (hybrid assemblies) [

Apart from eight HQ MAGs, we recovered three different MQ MAGs from potentially new species of the

A limitation of this study is the use of nanopore-only data since it can compromise the accuracy of the HQ MAGs, and the use of short-read polishing could have further improved the sequence accuracy. However, the combination of high-accuracy basecallers and raw reads correction, followed by further polishing of the metagenome assemblies increased the consensus accuracy to levels suitable to retrieve high-quality MAGs from a single fecal sample. In our case, we applied Guppy for basecalling, Canu for raw reads correction, and Medaka for polishing the assembled metagenomes. To reduce the insertion and deletion error type, we further applied a frameshift-aware correction step [

