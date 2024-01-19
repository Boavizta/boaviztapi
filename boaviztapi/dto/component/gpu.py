from typing import Optional

from boaviztapi.dto.component import ComponentDTO


class GPU(ComponentDTO):
    gpu_die_size: Optional[float] = None
    gpu_process: Optional[float] = None
    vram_capacity: Optional[int] = None
    vram_density: Optional[float] = None
    pcb_size: Optional[float] = None
    pcb_dim_x: Optional[float] = None
    pcb_dim_y: Optional[float] = None
    pcie: Optional[str] = None
