# GPU data sources

Reference material for populating and verifying `boaviztapi/data/crowdsourcing/gpu_specs.csv`.
See [Add a new GPU](gpu.md) for the column definitions themselves.

Every row should carry at least one URL in the `source` column. Prefer **primary**
sources (vendor datasheets, architecture whitepapers, OEM option guides) over tech
press articles, which are harder to audit and more likely to disappear.

## Die size → `die_surface`

`die_surface` is **not** the raw die area. It is the effective wafer area per die,
including kerf, circular-wafer edge losses and yield, as computed by
`_calculate_effective_area_on_circular_wafer()` in
`boaviztapi/models/component/gpu.py`. For a multi-die package it is
`effective_area(per_die_area) * unit`.

So what you need to source is the **raw die area in mm²** for a single compute die.

| Source | Use for |
|---|---|
| [TechPowerUp GPU Database](https://www.techpowerup.com/gpu-specs/) | Best per-SKU source: die size, transistor count, process node, memory config, board form factor. One page per SKU |
| [NVIDIA resources portal](https://resources.nvidia.com/) | Architecture whitepapers, e.g. [Hopper](https://resources.nvidia.com/en-us-data-center-overview/gtc22-whitepaper-hopper). Authoritative on die size and transistor count |
| [List of Nvidia GPUs](https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units) | Comprehensive die-size tables with references |
| [List of AMD GPUs](https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units) | Same, for AMD |
| [Chips and Cheese](https://chipsandcheese.com/) | Die-level analysis, essential for chiplet parts such as MI300X |
| [Locuza](https://locuza.substack.com/) | Annotated die-shot measurements |
| [SemiAnalysis](https://www.semianalysis.com/) | Reticle limits, multi-die packaging |

Wikipedia architecture pages, useful when a SKU is not listed individually:
[Pascal](https://en.wikipedia.org/wiki/Pascal_(microarchitecture)) ·
[Volta](https://en.wikipedia.org/wiki/Volta_(microarchitecture)) ·
[Turing](https://en.wikipedia.org/wiki/Turing_(microarchitecture)) ·
[Ampere](https://en.wikipedia.org/wiki/Ampere_(microarchitecture)) ·
[Ada Lovelace](https://en.wikipedia.org/wiki/Ada_Lovelace_(microarchitecture)) ·
[Hopper](https://en.wikipedia.org/wiki/Hopper_(microarchitecture)) ·
[Blackwell](https://en.wikipedia.org/wiki/Blackwell_(microarchitecture)) ·
[CDNA](https://en.wikipedia.org/wiki/CDNA_(microarchitecture)) ·
[RDNA 2](https://en.wikipedia.org/wiki/RDNA_2)

!!! tip "Consistency check"
    Two SKUs built on the same die must have identical `die_surface`. For example
    every GA100 part (A100 PCIe/SXM4, 40 GB and 80 GB) is 826 mm² of raw die and
    therefore `2876.29`, regardless of memory capacity or board type.

## VRAM capacity and die count → `vram`, `number`

`vram` is the capacity **of one card** in GB, never an instance or node total. For
a card that carries two GPUs, such as the Tesla K80, it is the card's total (24 GB),
not the 12 GB each GPU sees. `number` is the count of VRAM dies (HBM stacks, or
GDDR packages) on the card.

| Source | Use for |
|---|---|
| NVIDIA product pages: [A100](https://www.nvidia.com/en-us/data-center/a100/), [H100](https://www.nvidia.com/en-us/data-center/h100/), [H200](https://www.nvidia.com/en-us/data-center/h200/), [L4](https://www.nvidia.com/en-us/data-center/l4/), [P100](https://www.nvidia.com/en-us/data-center/tesla-p100/), [DGX B200](https://www.nvidia.com/en-us/data-center/dgx-b200/) | Capacity, bandwidth and memory type per SKU |
| [AMD Instinct](https://www.amd.com/en/products/accelerators/instinct.html) · [MI300X](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html) · [Radeon PRO](https://www.amd.com/en/products/accelerators/radeon-pro.html) | Official AMD specifications |
| [TechPowerUp GPU Database](https://www.techpowerup.com/gpu-specs/) | Memory bus width and chip count, from which `number` can be derived |

## Board power → `tdp`

`tdp` is the maximum board power of one card in W, as given by the vendor
(often "max power consumption", "max TDP power" or "total board power"). The
use phase models the power of one GPU from it (see
[GPU usage impacts](../Explanations/components/gpu.md#usage-impacts)).

| Source | Use for |
|---|---|
| Vendor product pages and datasheets, e.g. [L4](https://www.nvidia.com/en-us/data-center/l4/), [RTX PRO 4500 Server Edition](https://www.nvidia.com/en-us/data-center/rtx-pro-4500-blackwell-server-edition/), [A10G](https://d1.awsstatic.com/product-marketing/ec2/NVIDIA_AWS_A10G_DataSheet_FINAL_02_17_2022.pdf), [Tesla K80](https://nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/Tesla-K80-BoardSpec-07317-001-v05.pdf) | Primary source for the board power |
| [TechPowerUp GPU Database](https://www.techpowerup.com/gpu-specs/) | TDP per SKU, when the vendor page gives none |
| [flopper.io](https://flopper.io/gpus) | Cross-check of TDPs across many datacentre GPUs |
| [mirrorfrog](https://mirrorfrog.com/en/docs/cards/aws/inferentia/) | Accelerators for which the vendor publishes no TDP, such as AWS Inferentia and Trainium |

!!! warning "Use the variant the provider runs"
    Server, workstation and cloud-specific variants of a GPU can have very
    different TDPs: the RTX PRO 4500 Server Edition is 165 W but the workstation
    card is 200 W, and the A10G of AWS g5 instances is 300 W where the A10 is
    150 W. Check which variant the instance uses before picking a TDP.

!!! note
    A row without `tdp` falls back to the 700 W (range 70-1100 W) of the `DEFAULT` row of
    `boaviztapi/data/archetypes/components/gpu.csv`, a large datacentre GPU.

## GPUs per card → `gpus_per_card`

Most cards carry one GPU, and `gpus_per_card` is `1`. Some older cards carry two
GPUs on one board, which the operating system and the cloud providers see as two
GPUs: the Tesla M60, the Tesla K80 and the GRID K520. Set `gpus_per_card` to `2`
for them, and describe the whole card in the other columns (its `tdp`, `vram`,
masses, and `die_surface` as `effective_area(per_die_area) * unit`). The API then
divides the card's power and embodied impacts by `gpus_per_card` for each GPU.

A multi-die package that the providers count as one GPU, such as the B200 or the
MI300X, has `gpus_per_card` = `1` and `unit` greater than 1.

## Mass → `mass`, `mass_heatsink`, `mass_casing`

The hardest fields to source. Vendor briefs often omit weight, so OEM option
catalogues are usually the practical answer.

| Source | Use for |
|---|---|
| [Lenovo Press GPU options](https://lenovopress.lenovo.com/servers/options/gpu) | Best single source. Per-GPU product guides listing net weight and dimensions, e.g. [A100 PCIe](https://lenovopress.lenovo.com/lp1644-thinksystem-nvidia-a100-pcie-gpu), [RTX PRO 6000](https://lenovopress.lenovo.com/lp2263-thinksystem-nvidia-rtx-pro-6000-blackwell-server-edition-pcie-gen5-gpu) |
| NVIDIA product briefs | Some state weight directly (T4, A10, L40S, V100 PCIe, M60, P4 are sourced this way today) |
| HPE QuickSpecs, Dell PowerEdge manuals | Equivalent OEM data for cards Lenovo does not carry |

!!! warning "Empty mass fields are not neutral"
    A blank `mass`, `mass_heatsink` or `mass_casing` silently falls back to the
    `DEFAULT` row of `boaviztapi/data/archetypes/components/gpu.csv` — currently
    1.69 kg / 0.90 kg / 0.79 kg, i.e. a large datacentre card. That is a
    significant overestimate for single-slot or low-profile boards.

## PCB area → `pwb_surface`

In practice this is derived from the **card outline dimensions**, not a measured
PCB area, so the reference is the mechanical-dimensions section of a product
brief. Common form factors:

| Form factor | Dimensions | Area |
|---|---|---|
| Full-height, full-length (FHFL) | 111.15 × 266.7 mm | 296.4 cm² |
| Three-quarter length | 111.15 × 210.9 mm | 234.4 cm² |
| Half-height, half-length (short) | 68.9 × 135.2 mm | 93.1 cm² |
| SXM2 / SXM4 module | — | 109.2 / 105.0 cm² |

For SXM and OAM module footprints:
[SXM socket](https://en.wikipedia.org/wiki/SXM_(socket)) ·
[OCP Accelerator Module (OAM)](https://www.opencompute.org/projects/ocp-accelerator-module-oam)

!!! note
    `234.36` currently appears on 18 of 40 rows. It functions as a default for
    generic full-size PCIe cards rather than a per-card measurement. Treat it as a
    modelling assumption, not sourced data.

## Cloud instance ↔ GPU mapping

Not part of `gpu_specs.csv`, but these are the authority for which GPU SKU an
archetype in `boaviztapi/data/archetypes/server.csv` should name, and for how
many GPUs each instance has (`gpu_units`, counted the way the provider counts them).

| Provider | Reference |
|---|---|
| AWS | [Accelerated computing instance types](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html) |
| GCP | [GPU machine types](https://cloud.google.com/compute/docs/gpus) |
| Azure | [GPU-accelerated VM sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nvadsa10v5-series) |

## Citing sources in the CSV

Put one or more URLs in the `source` column, separated by `;`:

```csv
NVIDIA A100 PCIe 80GB,NVIDIA,1,6,80,2876.29,234.36,19000,1000,0,0.3,0.643,1.17,300,1,https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf;https://en.wikipedia.org/wiki/Ampere_(microarchitecture)
```

The value is surfaced through the API in the completion message for each
attribute, for example
`"Completed from name based on <source>."`, so a row left without a source
produces a message with no usable provenance.
