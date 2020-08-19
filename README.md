# AuToTen 


## Introduction

This is a **provisional** repository for AuToTen (as in **Au**tomatic **To**nal **Ten**sion), a Python-based system which automatically calculates the values of tonal tension of a piece of music according to Lerdahl's model of tonal tension. Please cite the following paper if you use AuToTen in your scientific work:

*add reference when published*

## Paper abstract

Since the early years of the past century, many scholars have focused their efforts towards designing models to better understand the way listeners perceive musical tension. From the existing models, Lerdahl’s has shown strong correlations against tension judgements provided by human listeners and has been used to make accurate predictions of musical tension. However, a full automation of Lerdahl’s model of tension has not yet been made available. This paper presents a computational approach to automatically calculate musical tension according to Lerdahl’s model, with a publicly available implementation.


## How to use AuToTen?


To fully operate AuToTen, the user should run `run.py`. A `tkinter` dialogue will ask the user to input the piece of music to be analysed, its *prolongational reduction* and its *metrical reduction*, all three in XML format. The *prolongonational reduction* and the *metrical reduction* are components of the Generative Theory of Tonal Music (GTTM). These must be calculated by the user, a priori, using the Interactive GTTM Analyser (IGA), which can be found at http://www.gttm.jp/. Please note IGA was not developed by AuToTen's authors, nor is hosted and maintained by them. We recommend storing the piece of music in such a way its melody is included in a single voice. This is because the current version of IGA produces more accurate results in this way. For example, see the directory */example* included in this repository. The files *example.xml*, *example-pr.xml* and *example-mr.xml* correspond to the piece of music to be analysed, its *prolongational reduction* and its *metrical reduction*, respectively.

`run.py` includes all the util functions embedded within AuToTen and it will directly calculate the values of *tension* and *attraction* of the input piece of music, according to Lerdahl's model of tonal tension. Likewise, these will be stored in two CSV files in your working folder. See, for example, *example-auto-tension.csv* and *example-auto-attraction.csv* in */example*.

Alternatively, the user can also call AuToTen's util functions independently. We recommend first running `setup.py`. In this way, the user will be able to directly call the following functions:

- `distance`, which calculates the distance between two chords in Lerdahl's Tonal Pitch Space (TPS).
- `t_calculator`, which calculates the values of *hierarchical tension* of a given piece of music according to Lerdahl's model of tonal tension. See, for example, *example-auto-tension.csv* in */example*.
- `a_calculator`, which calculates the values of *harmonic attraction* of a given piece of music according to Lerdahl's model of tonal tension. See, for example, *example-auto-attraction.csv* in */example*.
- `generator`, which calculates a representation, in the form of a matrix, of the piece's GTTM hierarchical analysis. See, for example, *example-auto-matrix.csv* in */example*.
- `offset`, which calculates the offset values of the events included in the piece's *metrical reduction*. See, for example, *example-auto-offsets.csv* in */example*.
- `parameters_finder`, which calculates the parameters needed for the calculation of tension according to Lerdahl's model of tonal tension. See, for example, *example-auto-piece-data.csv* in */example*.


## How does AuToTen work?

The workflow of AuToTen is shown in the figure below. As input, AuToTen is fed with a piece of music, in XML format, and it outputs its values of *global tension* and *attraction*. The unshaded boxes in the workflow represent the algorithms embedded in AuToTen, whereas the shaded boxes represent the corresponding inputs and outputs to these algorithms. There is also a box which has been highlighted with a dotted line. It represents the GTTM-based analysis that has to be performed using IGA.

![AuToTen's workflow](/images/workflow.png)
Format: ![Alt Text](url)

### AuToTen's implementation

To calculate the values of *tension* and *attraction* of a given piece of music, according to Lerdahl's model of tonal tension, AuToTen takes the following steps:

#### Step 1

*Identify the most probable patterns of strong and weak beats, and how might these be grouped, as well as the piece's most probable hierarchical relations according to GTTM rules.*

Recall this step needs to be performed by IGA's *GTTM tree analyser*. As input, it needs a piece of music, in XML format. As output, it produces the piece's hierarchical structure (*GTTM tree* in the above figure) and its metrical structure (*metre* in the above figure), both in XML format.


#### Step 2

*Define the musical events that will be assigned with a tension value, according to the analysis performed in the previous step.*

Step 2 is performed by the *metre analyser*. As input, it is fed with *metre*, calculated in Step 1. As output, it produces a list of the piece's *offsets*. These are interpreted by AuToTen as the list of the piece's beats which will be assigned with a value of tension and attraction.

In AuToTen, the *metre analyser* corresponds to `functions.metre.offset`. The input file, *metre*, provided by IGA, is stored as an *XML ElementTree*. In this tree, the offsets are labelled as *metric dots*. `functions.metre.offset` simply finds these *metric dots* and stores their offset values in a flat list.

#### Step 3

*Represent the hierarchical relations in such a way that will facilitate the calculation of tension (recall that this representation, in the case of manual calculations, is given in the form of a tree).*

Step 3 is performed by the *matrix calculator*. As input, it is fed with the *GTTM tree*, calculated in Step 1. As output, it produces a  *GTTM matrix*. This matrix is AuToTen's representation of the hierarchical relations embedded in a *GTTM tree*. 

In AuToTen, the *matrix calculator* corresponds to `functions.prolongation.generator`. The input file, *GTTM tree*, provided by IGA, is stored as an *XML ElementTree*. Be a *GTTM tree* with *n* events, `functions.prolongation.generator` will calculate its representation as a *n*x*n* *GTTM matrix*. A given event in the piece, *x*, will be represented in the *GTTM matrix* by the *xth* row, which will only contain a non-empty value, that coinciding with column *y*. An example is shown in the figure below. Note that the highest dominating event is number 5, as there are no branches above it. This will be denoted by a 0 at the (5,5) element in the *GTTM matrix*. The events that connect to 5 in the tree, these are events 1 and 4, are represented by a value of 1 in the *GTTM matrix* (i.e. there is only one branch above them) (see elements (1,5) and (4,5)). And so on. The rest of the elements in the *GTTM matrix* are kept empty. 

![GTTM matrix calculation example](/images/tree-example.png)
Format: ![Alt Text](url)

#### Step 4

*Perform a harmonic analysis of the defined musical events and label them accordingly (Roman Numeral analysis is the notation used all along Lerdahl's work).*

Step 4 is performed by the *harmonic analyser*. As input, it is fed with the piece of music, in XML format. As output, it calculates the most suitable *key* and *chord labels* of the piece's musical events.

In AuToTen, the *harmonic analyser* corresponds to `functions.variables.chords_components.chords_parameters`, which uses the toolkit *music21*. Given a piece of music, `functions.variables.chords_components.chords_parameters` estimates the piece's key using *music21*'s `analyze('key')`. Likewise, it estimates the most suitable key for each measure using `analyze` in every measure (i.e. `getElementsByClass('Measure')`). In this way, different versions of the chords' labels can be calculated. On the one hand, *music21*'s `chordify` is used to estimate the chords' labels using the whole piece's estimated key. On the other hand, `chordify` is used to estimate different versions of the chords' labels for every measure's key. These two different methods will allow better identification of non-diatonic chords, such as secondary dominants. 

Sometimes, *music21* identifies a chord which is missing its third. In this cases, *music21*'s `quality` will not identify the chord as being major, minor, augmented or diminished but as *other*. To deal with this issue, `functions.variables.chords_components.chords_parameters` will modify the corresponding chord labels so that they represent their respective diatonic version. 


#### Step 5

*Calculate the surface parameters for all musical events.*

Step 5 is performed by the *parameter calculator*. As input, it is fed with the list of *offsets*, calculated in Step 2, and the piece's *key* and its *chords*' labels, calculated in Step 4. As output, it produces the piece's values of *surface parameters*, needed to apply the rules in Lerdahl's model of tonal tension. These parameters concern the scale degree of the chords' highest note, the chords' inversions and the role the chords' notes play within the Tonal Pitch Space.

In AuToTen, the *parameter calculator* corresponds to `functions.variables.chords_components.chords_parameters` and `functions.surface.parameters_finder`. The former calculates the *surface parameters* for every different version of the chords labels estimated in Step 4. To do so, it uses *muisc21*'s `getScaleDegreeFromPitch`, `inversion` and  `pitches`, as well as the *surface parameters*' theoretical weightings defined in Lerdahl's model of tonal tension. The latter estimates the most appropriate chords labels and their corresponding *surface parameters*. To do so, `functions.surface.parameters_finder` compares the *surface parameter* that concerns the existence of non-harmonic notes in each chord and estimates the final chords labels that will suit the least non-harmonic musical discourse. Likewise, `functions.surface.parameters_finder` will correct any offset-related mismatching. Note that two different systems have been used to analyse the musical events in a given piece of music: IGA and *music21*. It might be the case where the number of events found by these two systems is not the same. AuToTen will be using the events calculated by IGA, as the prolongational relations in the *GTTM tree* are defined according to these events. So that, `functions.surface.parameters_finder` will compare IGA's offsets with those of *music21* and will assign the appropriate chord label and a set of *surface parameters* to each of IGA's offsets.


#### Step 6

*Calculate the values of global tension and attraction of all musical events.*

Finally, Step 6 is performed by the *tension calculator*. As input, it is fed with the *surface parameters*, the *chords*' labels and the *GTTM matrix*, calculated in Steps 5, 4 and 3, respectively. As output, it produces the values of *global tension* and *attraction*, according to Lerdahl's model of tonal tension, of all musical events in the input piece of music.


In AuToTen, the *tension calculator* corresponds to `functions.tension.t_calculator` and `functions.attraction.a_calculator`. Both functions need from the distance values between chords within TPS, which is given by `functions.tps.distance`. According to Lerdahl's model of tension, this distance, *d*, is computed as *d = i+j+k*, where *i* represents the distance between both chords in the chromatic circle-of-fifths, *j* represents the distance between both chords in the diatonic circle-of-fifths and *k* represents the difference between the representation of both chords within the Tonal Pitch space, known as *basic spaces*. Thus, `functions.tps.distance` calls the functions `functions.variables.tps_components.i`, `functions.variables.tps_components.j` and `functions.variables.tps_components.k`. To operate, these three functions need the *basic* and *chordal spaces* of the two input chords. These spaces are calculated through `functions.classes.space.Space`. The input chords, in Roman numeral format, are translated into the alphabet key-signature format in `functions.classes.parser`.  Their notes are then calculated by the `functions.classes.notes`. All the parameters needed for the calculations are included in `functions.parameters.common`.

`functions.tension.t_calculator` calculates the flow of *hierarchical tension* of a given piece of music. According to Lerdahl's model, the final value of *hierarchical tension* between two chords depends on the *surface parameters*, the TPS distance between chords and a collection of inherited distances that depends on the hierarchical structure defined by the *GTTM tree*. These three contributions are calculated using the functions `functions.variables.tension_components.dissonance`, `functions.tps.distance` and `functions.variables.tension_components.inherited`, respectively. For these functions to operate, they need the *GTTM matrix* and the *chords labels*, which are processed using `functions.classes.sequence.Harmony` and `functions.classes.matrix.Reduction`.

`functions.attraction.a_calculator` calculates the flow of *harmonic attraction* of a given piece of music. According to Lerdahl's model, the final value of *harmonic attraction* between two chords depends on the TPS distance between them, the intervals between their notes and their *anchoring spaces*, which are updated versions of the chords' *basic spaces*.


## How was AuToTen evaluated?


One hundred test cases were manually annotated to test the validity of AuToTen's calculations. Likewise, a computational evaluation was carried out using four pieces of music: Wagner’s Grail theme from Parsifal, Bach’s chorale “Christus, der ist mein Leben”, and harmonic reductions of Chopin’s E major prelude and the first phrase in Mozart’s sonata k.282. See *add paper's citation* for more detail. AuToTen's outputs showed strong and statistically significant correlations against all pieces, but that of Chopin's, the longest piece with many modulations, whose correlation was moderately strong.

The user can run the functions `tests.distance_tests` and `tests.tension_tests` to see how AuToTen's calculations agree with the ground-truths in all 100 cases.

The data used to produce the results of the test cases and the evaluation, as shown in *add paper's citation*, can be found in `/tests` and `/evaluation`, respectively.


## Where to find more information about the theoretical concepts upon which AuToTen is built on?


- Generative Theory of Tonal Music: https://music.columbia.edu/publications/books/a-generative-theory-of-tonal-music

- Tonal Pitch Space: https://music.columbia.edu/publications/books/tonal-pitch-space

- Lerdhal's model of tonal tension: https://online.ucpress.edu/mp/article/24/4/329/95267/Modeling-Tonal-Tension

- Interactive GTTM Analyser: http://www.gttm.jp/


