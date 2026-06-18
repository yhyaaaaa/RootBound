import hashlib
import os
import subprocess
import platform

class HardwareSRAM:
    """
    Derives a unique secret (Part B) from actual physical hardware identifiers.
    This makes the secret unique to the machine and not stored on disk.
    """
    def __init__(self):
        self.os_type = platform.system()

    def _get_hw_ids(self):
        """
        Retrieves unique hardware identifiers based on the operating system.
        """
        ids = []
        try:
            if self.os_type == "Windows":
                # Get Motherboard UUID
                uuid = subprocess.check_output('wmic csproduct get uuid', shell=True).decode().split('\n')[1].strip()
                # Get CPU ID
                cpu = subprocess.check_output('wmic cpu get processorid', shell=True).decode().split('\n')[1].strip()
                ids.extend([uuid, cpu])
            else:
                # Linux: Get product UUID from sysfs
                with open("/sys/class/dmi/id/product_uuid", "r") as f:
                    ids.append(f.read().strip())
                # Linux: Get CPU info
                cpu = subprocess.check_output('cat /proc/cpuinfo | grep "serial" | cut -d ":" -f 2', shell=True).decode().strip()
                if cpu: ids.append(cpu)
        except Exception as e:
            # Fallback to a machine-id if specific hardware calls fail
            try:
                if self.os_type == "Linux":
                    with open("/etc/machine-id", "r") as f: ids.append(f.read().strip())
                else:
                    ids.append(platform.node()) # Hostname as last resort
            except:
                ids.append("FALLBACK-ID-UNSTABLE")

        return "|".join(ids)

    def derive_part_b(self):
        """
        Calculates Part B on-the-fly based on actual hardware.
        """
        hw_string = self._get_hw_ids()
        # We hash the hardware string to create the secret Part B
        return hashlib.sha256(hw_string.encode()).digest()

    def wipe_memory(self, secret_ref):
        """
        Simulates the memory wipe.
        """
        if isinstance(secret_ref, bytearray):
            for i in range(len(secret_ref)):
                secret_ref[i] = 0
        return None
