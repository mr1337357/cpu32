----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/08/2023 01:00:32 PM
-- Design Name: 
-- Module Name: registers - Behavioral
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
use ieee.numeric_std.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity registers is
    Port ( clk : in STD_LOGIC;
           ra1 : in STD_LOGIC_VECTOR (4 downto 0);
           ra2 : in STD_LOGIC_VECTOR (4 downto 0);
           wa  : in STD_LOGIC_VECTOR (4 downto 0);
           we  : in STD_LOGIC;
           rd1 : out STD_LOGIC_VECTOR (31 downto 0);
           rd2 : out STD_LOGIC_VECTOR (31 downto 0);
           wd  : in STD_LOGIC_VECTOR (31 downto 0)
           );
end registers;

architecture Behavioral of registers is
    type regfile is array(31 downto 0) of std_logic_vector(31 downto 0);
    signal reg : regfile := (others => (others => '0'));
begin
    rd1 <= reg(to_integer(unsigned(ra1)));
    rd2 <= reg(to_integer(unsigned(ra2)));
    process(clk,wa,we,wd)
    begin
        if(rising_edge(clk))
        then
            if(we = '1')
            then
                reg(to_integer(unsigned(wa))) <= wd;
            end if;
        end if;
    end process;    
end Behavioral;
