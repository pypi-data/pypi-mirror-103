#  Copyright (c) 2019-2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""Communication protocols subpackage."""

from .base import (  # noqa: F401
    CommunicationProtocol,
    NullCommunicationProtocol,
)

try:
    from .labjack_ljm import (  # noqa: F401
        LJMCommunication,
        LJMCommunicationConfig,
        LJMCommunicationError,
    )
except (ImportError, ModuleNotFoundError):
    import warnings

    warnings.warn("To use libtiepie library install hvl with command "
                  "`pip install hvl_ccb[tiepie]`.")
from .modbus_tcp import (  # noqa: F401
    ModbusTcpCommunication,
    ModbusTcpConnectionFailedException,
    ModbusTcpCommunicationConfig,
)
from .opc import (  # noqa: F401
    OpcUaCommunication,
    OpcUaCommunicationConfig,
    OpcUaCommunicationIOError,
    OpcUaCommunicationTimeoutError,
    OpcUaSubHandler,
)
from .telnet import (  # noqa: F401
    TelnetCommunication,
    TelnetCommunicationConfig,
    TelnetError,
)
from .serial import (  # noqa: F401
    SerialCommunication,
    SerialCommunicationConfig,
    SerialCommunicationIOError,
)
from .visa import (  # noqa: F401
    VisaCommunication,
    VisaCommunicationError,
    VisaCommunicationConfig,
)
