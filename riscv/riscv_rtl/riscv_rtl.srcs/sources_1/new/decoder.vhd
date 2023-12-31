----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/08/2023 11:03:10 AM
-- Design Name: 
-- Module Name: decoder - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity decoder is
    Port (   inst : in  STD_LOGIC_VECTOR(31 downto 0);
           opcode : out STD_LOGIC_VECTOR( 6 downto 0);
               rd : out STD_LOGIC_VECTOR( 4 downto 0);
              rs1 : out STD_LOGIC_VECTOR( 4 downto 0);
              rs2 : out STD_LOGIC_VECTOR( 4 downto 0);
              imm : out STD_LOGIC_VECTOR(31 downto 0));
end decoder;

architecture Behavioral of decoder is
    type op_type is (R, I, S, B, U, J, X);
    signal op : std_logic_vector(4 downto 0);
    signal optype : op_type;
begin
    opcode <= inst(6 downto 0);
    op <= inst(6 downto 2);
    optype <= R when op = x"0C" else
              I when op = x"04" else
              S when op = x"08" else
              B when op = x"18" else
              U when op = x"0D" or op = x"05" else
              J when op = x"1b" else
        X;
    rd <= inst(11 downto 7);
    rs1 <= inst(19 downto 15);
    rs2 <= inst(24 downto 20);
    imm <= inst(31) & inst(31) & inst(31) & inst(31) & inst(31) & inst(30 downto 25) & inst(24 downto 21) & inst(20) when optype = I else
    (others => '0');

end Behavioral;
