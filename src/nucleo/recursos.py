class GestorRecursos:
    def __init__(self, total_cpu: int = 1, total_ram_mb: int = 4096):
        self.total_cpu = total_cpu
        self.total_ram_mb = total_ram_mb
        
        # Al iniciar, todos los recursos están libres
        self.cpu_libre = total_cpu
        self.ram_libre = total_ram_mb

    def solicitar(self, cpu_req: int, ram_req: int) -> tuple[bool, str]:
        """
        Intenta asignar recursos. 
        Retorna (True, "Mensaje de éxito") o (False, "Motivo del conflicto").
        """
        if self.cpu_libre < cpu_req:
            return False, f"Conflicto: CPU insuficiente. Solicitado: {cpu_req}, Libre: {self.cpu_libre}"
            
        if self.ram_libre < ram_req:
            return False, f"Conflicto: Memoria insuficiente. Solicitado: {ram_req} MB, Libre: {self.ram_libre} MB"
            
        # Asignación exitosa
        self.cpu_libre -= cpu_req
        self.ram_libre -= ram_req
        return True, "Recursos asignados correctamente."

    def liberar(self, cpu_liberada: int, ram_liberada: int):
        """Devuelve los recursos al pool cuando un proceso termina."""
        self.cpu_libre = min(self.total_cpu, self.cpu_libre + cpu_liberada)
        self.ram_libre = min(self.total_ram_mb, self.ram_libre + ram_liberada)