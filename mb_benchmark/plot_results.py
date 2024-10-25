import matplotlib.pyplot as plt


# make a dict with all the timings

data = {
    "N": [9306, 31641, 72618, 143181],
    "FESTIM 1.3": {
        "1": [12.2, 25.4, 52.6, float("nan")],
        "2": [
            4.866021394729614,
            13.057082176208496,
            28.47659468650818,
            52.7559278011322,
        ],
        "3": [37.6, 105, 299.2, 668.991974],
        "4": [
            44.28957200050354,
            128.98291850090027,
            267.6051115989685,
            806.8175826072693,
        ],
    },
    "fenicsx": {
        "1": [2.8, 12.7, 44.6, 199.255235],
        "2": [
            6.253011226654053,
            24.899581909179688,
            67.05651259422302,
            157.53219413757324,
        ],
        "3": [
            5.222760915756226,
            19.31188678741455,
            53.28000807762146,
            127.28776454925537,
        ],
        "4": [
            3.8878681659698486,
            14.572493076324463,
            42.534284591674805,
            105.31360197067261,
        ],
    },
    "fenicsx (hypre + boomeramg)": {
        "1": [
            15.452625751495361,
            51.295109272003174,
            118.5388457775116,
            245.65947127342224,
        ],
        "2": [
            11.6153883934021,
            37.571879386901855,
            86.74716210365295,
            177.6123344898224,
        ],
        "3": [
            8.914120435714722,
            27.79547929763794,
            63.01554274559021,
            127.95467472076416,
        ],
        "4": [
            6.676684141159058,
            20.92658805847168,
            49.486345052719116,
            95.33862400054932,
        ],
        "8": [
            4.775817394256592,
            13.935144424438477,
            30.67380118370056,
            61.05517888069153,
        ],
        "16": [
            5.267477750778198,
            13.24011754989624,
            29.41685652732849,
            54.021490812301636,
        ],
        "24": [
            9.141607284545898,
            19.470141887664795,
            33.23912048339844,
            34.85586881637573,
        ],
    },
    "fenicsx (gamg)": {
        "1": [
            14.785885572433472,
            48.1910138130188,
            107.47895312309265,
            211.26953411102295,
        ],
        "2": [
            11.09827446937561,
            35.21728706359863,
            79.33624529838562,
            154.45560455322266,
        ],
        "3": [
            8.231062650680542,
            25.879667043685913,
            55.819355964660645,
            107.8951997756958,
        ],
        "4": [
            6.105703115463257,
            18.866573810577393,
            43.294291734695435,
            81.0603539943695,
        ],
    },
}

# read the data from csv files called festim_1_results_nprocs_*.csv and festim_2_results_nprocs_*.csv
# and store them in the data dict
# 1. get the total number of cells by adding the nb_cells columns that have the same size for each rank
# 2. get time by taking one time of rank 0


fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 10), sharex=True)
nb_proc = [1, 2, 3, 4]
for N in data["N"]:
    plt.sca(ax[data["N"].index(N) // 2, data["N"].index(N) % 2])
    # title
    plt.title(f"N = {N}")
    festim_1_3 = [data["FESTIM 1.3"][str(i)][data["N"].index(N)] for i in nb_proc]
    plt.plot(
        nb_proc,
        festim_1_3,
        marker="o",
        label="1.3",
    )
    plt.plot(
        nb_proc,
        [data["fenicsx"][str(i)][data["N"].index(N)] for i in nb_proc],
        marker="o",
        label="fenicsx",
    )
    plt.plot(
        nb_proc,
        [data["fenicsx (gamg)"][str(i)][data["N"].index(N)] for i in nb_proc],
        marker="o",
        label="fenicsx (gamg)",
    )
    plt.plot(
        nb_proc,
        [
            data["fenicsx (hypre + boomeramg)"][str(i)][data["N"].index(N)]
            for i in nb_proc
        ],
        marker="o",
        label="fenicsx (hypre + boomeramg)",
    )
    plt.ylim(bottom=0)

ax[0, 0].legend()
ax[0, 0].set_xticks(nb_proc)
ax[0, 0].set_ylabel("Time (s)")
ax[1, 0].set_ylabel("Time (s)")
ax[1, 0].set_xlabel("Number of processes")
ax[1, 1].set_xlabel("Number of processes")

plt.figure()
for solver in ["fenicsx", "fenicsx (hypre + boomeramg)", "fenicsx (gamg)"]:
    plt.plot(data["N"], data[solver]["4"], label=solver, marker="o")

plt.legend()
plt.xlabel("Number of cells")
plt.ylabel("Time (s)")

fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 10), sharex=True)
nb_proc = [int(nb) for nb in data["fenicsx (hypre + boomeramg)"].keys()]
for N in data["N"]:
    plt.sca(ax[data["N"].index(N) // 2, data["N"].index(N) % 2])
    # title
    plt.title(f"N = {N}")
    plt.plot(
        nb_proc,
        [
            data["fenicsx (hypre + boomeramg)"][str(i)][data["N"].index(N)]
            for i in nb_proc
        ],
        marker="o",
        label="fenicsx (hypre + boomeramg)",
    )
    plt.ylim(bottom=0)

ax[0, 0].legend()
ax[0, 0].set_ylabel("Time (s)")
ax[1, 0].set_ylabel("Time (s)")
ax[1, 0].set_xlabel("Number of processes")
ax[1, 1].set_xlabel("Number of processes")
ax[0, 0].set_xticks(nb_proc)
plt.show()
